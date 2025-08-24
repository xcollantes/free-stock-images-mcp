#!/usr/bin/env python3
"""Example usage of the free stock images MCP server."""

import asyncio
import sys
import os

# Add the server module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from server import search_stock_images, get_stock_image_sources, STOCK_IMAGE_SOURCES

async def example_search():
    """Example: Search for stock images."""
    print("🔍 Searching for 'sunset' images...")
    print("-" * 40)
    
    result = await search_stock_images({
        "query": "sunset",
        "sources": ["unsplash", "pexels", "pixabay"],
        "limit": 2
    })
    
    for item in result:
        print(item.text)
        print()

async def example_get_sources():
    """Example: Get available sources."""
    print("📋 Available stock image sources:")
    print("-" * 40)
    
    result = await get_stock_image_sources()
    
    for item in result:
        print(item.text)

def example_direct_access():
    """Example: Direct access to source information."""
    print("🔧 Direct access to source information:")
    print("-" * 40)
    
    for source_id, source_info in STOCK_IMAGE_SOURCES.items():
        print(f"Source ID: {source_id}")
        print(f"Name: {source_info['name']}")
        print(f"Description: {source_info['description']}")
        print(f"Base URL: {source_info['base_url']}")
        print()

async def main():
    """Run all examples."""
    print("Free Stock Images MCP Server - Example Usage")
    print("=" * 50)
    
    # Example 1: Direct access
    example_direct_access()
    
    # Example 2: Get sources using the function
    await example_get_sources()
    print()
    
    # Example 3: Search for images
    await example_search()
    
    print("=" * 50)
    print("✨ Examples completed!")

if __name__ == "__main__":
    asyncio.run(main())