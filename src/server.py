"""Free Stock Images MCP Server.

Provides access to free stock image sources including Unsplash, Pexels, Pixabay,
and others.
"""

import asyncio
import json
import logging
import os
import urllib.parse
from typing import Any, Dict, List, Optional

import requests
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Resource, TextContent, Tool
from pydantic import AnyUrl

# Configure logging.
logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

server: Server = Server(__name__)


# Free stock image sources with API configurations
STOCK_IMAGE_SOURCES: Dict[str, Dict[str, str]] = {
    "unsplash": {
        "name": "Unsplash",
        "base_url": "https://unsplash.com/s/photos/",
        "api_url": "https://api.unsplash.com/search/photos",
        "description": "Beautiful free photos & images",
        "requires_api_key": "true",
        "api_key_env": "UNSPLASH_ACCESS_KEY",
    },
    "pexels": {
        "name": "Pexels",
        "base_url": "https://www.pexels.com/search/",
        "api_url": "https://api.pexels.com/v1/search",
        "description": "Free stock photos & royalty free images",
        "requires_api_key": "true",
        "api_key_env": "PEXELS_API_KEY",
    },
    "pixabay": {
        "name": "Pixabay",
        "base_url": "https://pixabay.com/images/search/",
        "api_url": "https://pixabay.com/api/",
        "description": "Stunning royalty-free images & royalty-free stock",
        "requires_api_key": "true",
        "api_key_env": "PIXABAY_API_KEY",
    },
    "freepik": {
        "name": "Freepik",
        "base_url": "https://www.freepik.com/search?format=search&query=",
        "api_url": None,  # No public API available
        "description": "Free vectors, stock photos, PSD and icons",
        "requires_api_key": "false",
    },
    "burst": {
        "name": "Burst by Shopify",
        "base_url": "https://burst.shopify.com/photos/search?q=",
        "api_url": None,  # No public API available
        "description": "Free stock photos for commercial use",
        "requires_api_key": "false",
    },
    "stockvault": {
        "name": "StockVault",
        "base_url": "https://www.stockvault.net/search/?q=",
        "api_url": None,  # No public API available
        "description": "Free graphics and photos",
        "requires_api_key": "false",
    },
}


def make_api_request(source_id: str, query: str, limit: int = 5) -> Optional[Dict]:
    """Make API request to stock image service.

    Args:
        source_id: The ID of the stock image source
        query: Search query
        limit: Maximum number of results

    Returns:
        API response data or None if API call fails
    """
    source = STOCK_IMAGE_SOURCES.get(source_id)
    if not source or not source.get("api_url"):
        return None

    api_url = source["api_url"]
    api_key_env = source.get("api_key_env")

    # Check if API key is required and available
    if source.get("requires_api_key") == "true":
        if not api_key_env:
            logger.warning(f"No API key environment variable specified for {source_id}")
            return None

        api_key = os.getenv(api_key_env)
        if not api_key:
            logger.warning(f"API key not found in environment variable {api_key_env}")
            return None
    else:
        api_key = None

    try:
        # Prepare headers and params based on service
        headers = {"User-Agent": "free-stock-images-mcp/0.1.0"}
        params = {"q": query, "per_page": min(limit, 20)}

        if source_id == "unsplash" and api_key:
            headers["Authorization"] = f"Client-ID {api_key}"
            params = {"query": query, "per_page": min(limit, 30)}

        elif source_id == "pexels" and api_key:
            headers["Authorization"] = api_key
            params = {"query": query, "per_page": min(limit, 80)}

        elif source_id == "pixabay" and api_key:
            params = {"key": api_key, "q": query, "per_page": min(limit, 200)}

        logger.info(f"Making API request to {source_id}: {api_url}")
        response = requests.get(api_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:
        logger.error(f"API request failed for {source_id}: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response from {source_id}: {e}")
        return None


def format_api_results(source_id: str, api_data: Dict, query: str) -> str:
    """Format API response data into readable text.

    Args:
        source_id: The ID of the stock image source
        api_data: Raw API response data
        query: Original search query

    Returns:
        Formatted text with image information
    """
    source = STOCK_IMAGE_SOURCES[source_id]
    result_text = f"\n{source['name']} (API Results)\n"
    result_text += f"Description: {source['description']}\n\n"

    try:
        if source_id == "unsplash":
            results = api_data.get("results", [])
            for i, img in enumerate(results[:5], 1):
                result_text += f"{i}. {img.get('description', 'Untitled')}\n"
                result_text += f"- URL: {img['urls']['regular']}\n"
                result_text += f"- Download: {img['links']['download']}\n"
                result_text += f"- Author: {img['user']['name']}\n"
                result_text += f"- Dimensions: {img['width']}x{img['height']}\n\n"

        elif source_id == "pexels":
            photos = api_data.get("photos", [])
            for i, img in enumerate(photos[:5], 1):
                result_text += f"{i}. Photo #{img['id']}\n"
                result_text += f"- URL: {img['src']['large']}\n"
                result_text += f"- Medium: {img['src']['medium']}\n"
                result_text += f"- Photographer: {img['photographer']}\n"
                result_text += f"- Dimensions: {img['width']}x{img['height']}\n\n"

        elif source_id == "pixabay":
            hits = api_data.get("hits", [])
            for i, img in enumerate(hits[:5], 1):
                result_text += f"{i}. {img.get('tags', 'Untagged')}\n"
                result_text += f"- URL: {img['webformatURL']}\n"
                result_text += f"- Large: {img.get('largeImageURL', 'N/A')}\n"
                result_text += f"- User: {img['user']}\n"
                result_text += (
                    f"- Dimensions: {img['imageWidth']}x{img['imageHeight']}\n\n"
                )

    except KeyError as e:
        logger.error(f"Error parsing {source_id} API response: {e}")
        result_text += f"Error parsing API response: {e}\n"

    return result_text


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
        Tool(
            name="check_api_status",
            description="Check API key configuration status for stock image sources",
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

    elif name == "check_api_status":
        return await check_api_status()

    else:
        raise ValueError(f"Unknown tool: {name}")


async def search_stock_images(arguments: Dict[str, Any]) -> List[TextContent]:
    """Search for stock images from multiple sources using APIs when available.

    Args:
        arguments: A dictionary containing the search query, sources, and limit.

    Returns:
        A list of TextContent objects containing the search results.
    """
    query: str = arguments.get("query", "")
    sources: List[str] = arguments.get("sources", list(STOCK_IMAGE_SOURCES.keys()))
    limit: int = arguments.get("limit", 5)

    if not query:
        return [TextContent(type="text", text="Error: Search query is required")]

    results: List[TextContent] = []
    results.append(
        TextContent(type="text", text=f"# Stock Image Search Results for '{query}'\n")
    )

    api_sources = []
    web_sources = []

    for source_id in sources:
        if source_id not in STOCK_IMAGE_SOURCES:
            continue

        source = STOCK_IMAGE_SOURCES[source_id]

        # Try API integration first
        api_data = make_api_request(source_id, query, limit)

        if api_data:
            # Use API results
            api_sources.append(source_id)
            formatted_results = format_api_results(source_id, api_data, query)
            results.append(TextContent(type="text", text=formatted_results))
        else:
            # Fall back to web search links
            web_sources.append(source_id)
            encoded_query = urllib.parse.quote(query)
            search_url = f"{source['base_url']}{encoded_query}"

            results.append(
                TextContent(
                    type="text",
                    text=f"\n## {source['name']} (Web Search)\n"
                    f"**Description:** {source['description']}\n"
                    f"**Search URL:** {search_url}\n"
                    f"**Direct Link:** [Search '{query}' on {source['name']}]({search_url})\n",
                )
            )

    # Summary
    summary_text = f"\n---\n**Search Summary**\n"
    summary_text += f"**Query:** {query}\n"
    summary_text += f"**Total Sources:** {len(sources)}\n"

    if api_sources:
        summary_text += f"**API Integration:** {', '.join(api_sources)} ({len(api_sources)} sources)\n"
    if web_sources:
        summary_text += f"**Web Search Links:** {', '.join(web_sources)} ({len(web_sources)} sources)\n"

    summary_text += f"\n**Note:** For API sources, configure environment variables (UNSPLASH_ACCESS_KEY, PEXELS_API_KEY, PIXABAY_API_KEY) to get actual image data. "
    summary_text += f"Always check license requirements before using images."

    results.append(TextContent(type="text", text=summary_text))

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


async def check_api_status() -> List[TextContent]:
    """Check API key configuration status for all sources.

    Returns:
        A list of TextContent objects showing API configuration status.
    """
    content: List[str] = ["# API Configuration Status\n\n"]

    for source_id, source_info in STOCK_IMAGE_SOURCES.items():
        content.append(f"## {source_info['name']}\n")

        api_url = source_info.get("api_url")
        requires_key = source_info.get("requires_api_key") == "true"
        api_key_env = source_info.get("api_key_env")

        if not api_url:
            content.append("❌ **API Status:** No public API available\n")
            content.append("🔗 **Fallback:** Web search links only\n\n")
            continue

        content.append(f"✅ **API Endpoint:** {api_url}\n")

        if requires_key:
            if not api_key_env:
                content.append("❌ **API Key:** Environment variable not configured\n")
            else:
                api_key = os.getenv(api_key_env)
                if api_key:
                    # Mask the key for security
                    masked_key = api_key[:8] + "..." if len(api_key) > 8 else "***"
                    content.append(
                        f"✅ **API Key ({api_key_env}):** Configured ({masked_key})\n"
                    )
                else:
                    content.append(
                        f"❌ **API Key ({api_key_env}):** Not found in environment\n"
                    )
        else:
            content.append("✅ **API Key:** Not required\n")

        content.append("\n")

    # Configuration instructions
    content.append("---\n\n")
    content.append("## Configuration Instructions\n\n")
    content.append("To enable API integration, set these environment variables:\n\n")

    for source_id, source_info in STOCK_IMAGE_SOURCES.items():
        if source_info.get("requires_api_key") == "true":
            env_var = source_info.get("api_key_env")
            if env_var:
                content.append(
                    f"- **{source_info['name']}:** `export {env_var}=your_api_key_here`\n"
                )

    content.append(
        "\n**Note:** API keys provide richer data including image URLs, metadata, and direct download links.\n"
    )
    content.append(
        "Without API keys, the service falls back to providing web search links.\n"
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
