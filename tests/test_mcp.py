"""Starts the real MCP server as a separate process and calls its tools."""
import asyncio
import json
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters

ROOT = Path(__file__).parent.parent


def test_mcp_tools():
    async def run():
        params = StdioServerParameters(command=sys.executable, args=["mcp_server.py"], cwd=str(ROOT))
        async with Client(params) as client:
            tools = await client.list_tools()
            names = {t.name for t in tools.tools}
            requirement = {"id": "R1", "parameter": "bus_current_a", "value_number": 4000, "unit": "A"}
            result = await client.call_tool(
                "check_requirements", {"product_id": "MVA-15-3000", "requirements": [requirement]}
            )
            return names, result

    names, result = asyncio.run(run())
    assert names == {"search_catalog", "check_requirements"}
    data = result.structured_content or json.loads(result.content[0].text)
    assert data["mandatory_fails"] == 1
