"""Lets any MCP app, such as Claude Desktop, use the catalog and checks.

Run it with: python mcp_server.py
"""
from mcp.server.mcpserver import MCPServer

from speccheck.catalog import by_type, find_product, load_catalog
from speccheck.checks import check_product
from speccheck.models import Requirement

CATALOG = load_catalog()
server = MCPServer("speccheck")


@server.tool()
def search_catalog(equipment_type: str) -> list[dict]:
    """List products. equipment_type is mv_switchgear or lv_switchgear."""
    return by_type(CATALOG, equipment_type)


@server.tool()
def check_requirements(product_id: str, requirements: list[Requirement]) -> dict:
    """Check a product against a list of requirements."""
    product = find_product(CATALOG, product_id)
    if product is None:
        raise ValueError(f"Unknown product: {product_id}")
    check = check_product(requirements, product)
    return {
        "product_id": product_id,
        "mandatory_fails": check.mandatory_fails,
        "preferred_misses": check.preferred_misses,
        "needs_review": check.reviews,
        "results": [r.model_dump() for r in check.results],
    }


if __name__ == "__main__":
    server.run("stdio")
