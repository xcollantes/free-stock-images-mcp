"""Free Stock Images MCP Server.

Provides access to free stock image sources including Unsplash, Pexels, Pixabay,
and others.
"""

import asyncio
import logging
import urllib.parse
from typing import Any

from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Resource, TextContent, Tool
from pydantic import AnyUrl

# Configure logging.
logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

server: Server = Server(__name__)


# Free stock image sources.
STOCK_IMAGE_SOURCES: dict[str, dict[str, str]] = {
    "unsplash": {
        "name": "Unsplash",
        "base_url": "https://unsplash.com/s/photos/",
        "description": "Free photos and images",
    },
    "pexels": {
        "name": "Pexels",
        "base_url": "https://www.pexels.com/search/",
        "description": "Free photos and images",
    },
    "pixabay": {
        "name": "Pixabay",
        "base_url": "https://pixabay.com/images/search/",
        "description": "Free photos and images",
    },
    "freepik": {
        "name": "Freepik",
        "base_url": "https://www.freepik.com/search?format=search&query=",
        "description": "Free vectors, stock photos, PSD, and icons",
    },
    "burst": {
        "name": "Burst by Shopify",
        "base_url": "https://burst.shopify.com/photos/search?q=",
        "description": "Free stock photos for commercial use",
    },
    "stockvault": {
        "name": "StockVault",
        "base_url": "https://www.stockvault.net/search/?q=",
        "description": "Free graphics and photos",
    },
}


@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available stock image sources.

    Returns:
        A list of Resource objects containing the available stock image sources.
    """

    resources = []

    for source_id, source_info in STOCK_IMAGE_SOURCES.items():
        resources.append(
            Resource(
                uri=AnyUrl(f"stock-images://{source_id}"),
                name=f"{source_info['name']} Stock Images",
                description=source_info["description"],
                mimeType="text/plain",
            )
        )

    return resources


@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """Read resource content for stock image sources.

    Args:
        uri: The URI of the resource to read.

    Returns:
        A string containing the content of the resource.
    """

    if not str(uri).startswith("stock-images://"):
        raise ValueError(f"Unknown resource: {uri}")

    source_id = str(uri).replace("stock-images://", "")

    if source_id not in STOCK_IMAGE_SOURCES:
        raise ValueError(f"Unknown stock image source: {source_id}")

    source = STOCK_IMAGE_SOURCES[source_id]

    return f"""# {source['name']}

{source['description']}

Base URL: {source['base_url']}

To search for images, use the search_stock_images tool with this source.
"""


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools.

    Returns:
        A list of Tool objects containing the available tools.
    """

    return [
        Tool(
            name="search_stock_images",
            description="Search for free stock images from multiple sources",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for stock images",
                    },
                    "sources": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": list(STOCK_IMAGE_SOURCES.keys()),
                        },
                        "description": "Stock image sources to search (default: all sources)",
                        "default": list(STOCK_IMAGE_SOURCES.keys()),
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results per source (default: 5)",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 20,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_stock_image_sources",
            description="Get information about available free stock image sources",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[TextContent]:
    """Handle tool calls.

    Args:
        name: The name of the tool to call.
        arguments: A dictionary containing the arguments for the tool.

    Returns:
        A list of TextContent objects containing the tool call results.
    """

    if name == "search_stock_images":
        return await search_stock_images(arguments or {})

    elif name == "get_stock_image_sources":
        return await get_stock_image_sources()

    else:
        raise ValueError(f"Unknown tool: {name}")


async def search_stock_images(arguments: dict[str, Any]) -> list[TextContent]:
    """Search for stock images from multiple sources.

    Args:
        arguments: A dictionary containing the search query, sources, and limit.

    Returns:
        A list of TextContent objects containing the search results.
    """

    query = arguments.get("query", "")
    sources = arguments.get("sources", list(STOCK_IMAGE_SOURCES.keys()))
    limit = arguments.get("limit", 5)

    if not query:
        return [TextContent(type="text", text="Error: Search query is required")]

    results = []
    results.append(
        TextContent(type="text", text=f"# Stock Image Search Results for '{query}'\n")
    )

    for source_id in sources:
        if source_id not in STOCK_IMAGE_SOURCES:
            continue

        source = STOCK_IMAGE_SOURCES[source_id]
        encoded_query = urllib.parse.quote(query)
        search_url = f"{source['base_url']}{encoded_query}"

        results.append(
            TextContent(
                type="text",
                text=f"\n## {source['name']}\n"
                f"Description: {source['description']}\n"
                f"Search URL: {search_url}\n"
                f"Direct Link: [Search '{query}' on {source['name']}]({search_url})\n",
            )
        )

    results.append(
        TextContent(
            type="text",
            text=f"\n---\n"
            f"Total Sources: {len(sources)}\n"
            f"Search Query: {query}\n"
            f"Tip: Click the links above to browse and download free stock images. "
            f"Always check the license requirements for each image before use.",
        )
    )

    return results


async def get_stock_image_sources() -> list[TextContent]:
    """Get information about available stock image sources.

    Returns:
        A list of TextContent objects containing the information about the
        available stock image sources.
    """

    content = ["Available Free Stock Image Sources\n"]

    for source_id, source_info in STOCK_IMAGE_SOURCES.items():
        content.append(f"## {source_info['name']}\n")
        content.append(f"ID: `{source_id}`\n")
        content.append(f"Description: {source_info['description']}\n")
        content.append(f"Base URL: {source_info['base_url']}\n")
        content.append("\n")

    content.append("---\n")
    content.append(f"Total Sources: {len(STOCK_IMAGE_SOURCES)}\n")
    content.append(
        "Usage: Use the `search_stock_images` tool to search across these sources.\n"
    )

    return [TextContent(type="text", text="".join(content))]


async def main():
    """Run the server."""

    async with stdio_server() as (read_stream, write_stream):

        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="free-stock-images-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
