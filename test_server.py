#!/usr/bin/env python3
"""Test script for the free stock images MCP server."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'free_stock_images_mcp'))

def test_imports():
    """Test that all imports work."""
    try:
        from server import (
            STOCK_IMAGE_SOURCES,
            search_stock_images,
            get_stock_image_sources
        )
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_stock_sources():
    """Test that stock image sources are properly configured."""
    from server import STOCK_IMAGE_SOURCES
    
    required_fields = ['name', 'base_url', 'description']
    
    print(f"✓ Found {len(STOCK_IMAGE_SOURCES)} stock image sources:")
    
    for source_id, source_info in STOCK_IMAGE_SOURCES.items():
        print(f"  - {source_id}: {source_info['name']}")
        
        for field in required_fields:
            if field not in source_info:
                print(f"✗ Missing field '{field}' in source '{source_id}'")
                return False
        
        if not source_info['base_url'].startswith(('http://', 'https://')):
            print(f"✗ Invalid base_url in source '{source_id}': {source_info['base_url']}")
            return False
    
    print("✓ All stock image sources properly configured")
    return True

async def test_search_function():
    """Test the search function."""
    try:
        from server import search_stock_images
        
        # Test basic search
        result = await search_stock_images({
            "query": "test",
            "sources": ["unsplash", "pexels"],
            "limit": 2
        })
        
        if not result or not isinstance(result, list):
            print("✗ search_stock_images did not return a list")
            return False
        
        print("✓ search_stock_images function works")
        return True
        
    except Exception as e:
        print(f"✗ Error in search function: {e}")
        return False

async def test_sources_function():
    """Test the get sources function."""
    try:
        from server import get_stock_image_sources
        
        result = await get_stock_image_sources()
        
        if not result or not isinstance(result, list):
            print("✗ get_stock_image_sources did not return a list")
            return False
        
        print("✓ get_stock_image_sources function works")
        return True
        
    except Exception as e:
        print(f"✗ Error in get sources function: {e}")
        return False

async def main():
    """Run all tests."""
    print("Testing Free Stock Images MCP Server...")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 4
    
    # Test imports
    if test_imports():
        tests_passed += 1
    
    # Test stock sources configuration
    if test_stock_sources():
        tests_passed += 1
    
    # Test search function
    if await test_search_function():
        tests_passed += 1
    
    # Test sources function  
    if await test_sources_function():
        tests_passed += 1
    
    print("=" * 50)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Server is ready to use.")
        return True
    else:
        print("❌ Some tests failed. Please check the server implementation.")
        return False

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(main())
    sys.exit(0 if success else 1)