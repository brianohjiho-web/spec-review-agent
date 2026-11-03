"""Runs the agent through the real Anthropic SDK with fake server replies.

No API key is needed. These tests check the tool loop, not Claude's reading skill.
"""
import json
from pathlib import Path

import anthropic
import httpx2
import pytest

from speccheck.agent import TOOLS, AgentError, SpecAgent
from speccheck.catalog import load_catalog
from speccheck.pdf import read_pdf

SAMPLES = Path(__file__).parent.parent / "data" / "samples"
SPEC_TEXT = read_pdf((SAMPLES / "red_oak_mv.pdf").read_bytes())
REQUIREMENTS = json.loads((SAMPLES / "red_oak_mv.requirements.json").read_text())


def reply(stop_reason, *blocks):
    return {"id": "msg_1", "type": "message", "role": "assistant", "model": "claude-sonnet-5-5",
            "content": list(blocks), "stop_reason": stop_reason, "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1}}


def tool(name, tool_input, tool_id="t1"):
    return {"type": "tool_use", "id": tool_id, "name": name, "input": tool_input}


THINKING = {"type": "thinking", "thinking": "", "signature": "sig123"}


def make_agent(replies, catalog=None):
    requests = []

    def handler(request):
        requests.append(json.loads(request.content))
        return httpx2.Response(200, json=replies.pop(0))

    client = anthropic.Anthropic(api_key="test", http_client=httpx2.Client(transport=httpx2.MockTransport(handler)))
    return SpecAgent(catalog or load_catalog(), client=client), requests


def happy_path():
    return [
        reply("tool_use", THINKING, tool("save_requirements", REQUIREMENTS)),
        reply("tool_use", tool("search_catalog", {"equipment_type": "mv_switchgear"}, "t2")),
        reply("tool_use", tool("check_product", {"product_id": "MVA-15-3000"}, "t3"),
              tool("check_product", {"product_id": "MVA-15-4000"}, "t4")),
        reply("tool_use", tool("submit_review", {"summary": "Good fit.", "customer_questions": ["Which plant?"]}, "t5")),
    ]


def test_full_review():
    agent, requests = make_agent(happy_path())
    review = agent.run(SPEC_TEXT)
    assert review.recommended_id is None
    assert any(r.requirement.mandatory and r.status == "REVIEW" for r in review.ranked[0].results)
    assert review.summary == "Good fit."
    assert review.source == "claude"
    assert len(requests) == 4


def test_request_follows_the_api_rules():
    agent, requests = make_agent(happy_path())
    agent.run(SPEC_TEXT)
    first = requests[0]
    assert first["model"] == "claude-sonnet-5-5"
    assert first["tool_choice"] == {"type": "auto"}
    assert "temperature" not in first
    assert all(t["strict"] for t in first["tools"])


def test_thinking_blocks_are_sent_back_unchanged():
    agent, requests = make_agent(happy_path())
    agent.run(SPEC_TEXT)
    assistant_turn = requests[1]["messages"][1]
    assert assistant_turn["content"][0] == THINKING


def test_parallel_tool_calls_return_in_one_message():
    agent, requests = make_agent(happy_path())
    agent.run(SPEC_TEXT)
    results = requests[3]["messages"][-1]["content"]
    assert [r["tool_use_id"] for r in results] == ["t3", "t4"]


def test_spec_text_is_marked_as_data():
    agent, requests = make_agent(happy_path())
    agent.run(SPEC_TEXT)
    assert "<customer_spec>" in requests[0]["messages"][0]["content"]


def test_claude_cannot_override_the_python_result():
    replies = happy_path()
    replies[-1] = reply("tool_use", tool("submit_review", {"summary": "Pick MVA-15-4000!", "customer_questions": []}, "t5"))
    agent, _ = make_agent(replies)
    assert agent.run(SPEC_TEXT).recommended_id is None


def test_invented_requirement_is_flagged():
    bad = json.loads(json.dumps(REQUIREMENTS))
    bad["requirements"][2]["source_quote"] = "rated 1000 A continuous"
    bad["requirements"][2]["value_number"] = 1000
    replies = happy_path()
    replies[0] = reply("tool_use", tool("save_requirements", bad))
    agent, _ = make_agent(replies)
    top = agent.run(SPEC_TEXT).ranked[0]
    flagged = next(r for r in top.results if r.requirement.id == "R3")
    assert flagged.status == "REVIEW"


def test_unknown_product_is_returned_as_a_tool_error():
    replies = happy_path()
    replies[2] = reply("tool_use", tool("check_product", {"product_id": "FAKE"}, "t3"))
    agent, requests = make_agent(replies)
    agent.run(SPEC_TEXT)
    result = requests[3]["messages"][-1]["content"][0]
    assert result["is_error"] is True and "FAKE" in result["content"]


def test_bad_tool_input_is_returned_as_a_tool_error():
    replies = happy_path()
    replies.insert(0, reply("tool_use", tool("save_requirements", {"equipment_type": "toaster", "requirements": []})))
    agent, requests = make_agent(replies)
    agent.run(SPEC_TEXT)
    assert requests[1]["messages"][-1]["content"][0]["is_error"] is True


def test_submit_before_saving_is_rejected():
    replies = happy_path()
    replies.insert(0, reply("tool_use", tool("submit_review", {"summary": "x", "customer_questions": []})))
    agent, requests = make_agent(replies)
    assert agent.run(SPEC_TEXT).summary == "Good fit."
    assert requests[1]["messages"][-1]["content"][0]["is_error"] is True


def test_plain_text_answer_gets_one_reminder():
    replies = happy_path()
    replies.insert(0, reply("end_turn", {"type": "text", "text": "Looks fine."}))
    agent, _ = make_agent(replies)
    assert agent.run(SPEC_TEXT).recommended_id is None


def test_second_plain_text_answer_stops():
    text = {"type": "text", "text": "Looks fine."}
    agent, _ = make_agent([reply("end_turn", text), reply("end_turn", text)])
    with pytest.raises(AgentError):
        agent.run(SPEC_TEXT)


@pytest.mark.parametrize("stop_reason", ["max_tokens", "refusal"])
def test_early_stop_is_an_error(stop_reason):
    agent, _ = make_agent([reply(stop_reason, {"type": "text", "text": "..."})])
    with pytest.raises(AgentError, match=stop_reason):
        agent.run(SPEC_TEXT)


def test_endless_loop_stops():
    replies = [reply("tool_use", tool("search_catalog", {"equipment_type": "mv_switchgear"})) for _ in range(20)]
    agent, requests = make_agent(replies)
    with pytest.raises(AgentError):
        agent.run(SPEC_TEXT)
    assert len(requests) == 15


def test_strict_tool_schemas_are_well_formed():
    def walk(schema):
        if schema.get("type") == "object":
            assert schema["additionalProperties"] is False
            assert set(schema["required"]) == set(schema["properties"])
            for child in schema["properties"].values():
                walk(child)
        if "items" in schema:
            walk(schema["items"])

    for definition in TOOLS:
        walk(definition["input_schema"])
