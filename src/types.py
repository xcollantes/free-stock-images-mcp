"""Type definitions for the Free Stock Images MCP Server."""

from typing import Dict, List, Optional, TypedDict


class StockImageSource(TypedDict):
    """Type definition for stock image source configuration."""

    name: str
    base_url: str
    description: str


class SearchArguments(TypedDict, total=False):
    """Type definition for search tool arguments."""

    query: str
    sources: Optional[List[str]]
    limit: Optional[int]


# Type alias for readability.
StockImageSourcesDict = Dict[str, StockImageSource]
