#!/usr/bin/env python3
"""Example of using the enhanced API features."""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from server import make_api_request, format_api_results

def demo_api_integration():
    """Demonstrate API integration with different scenarios."""
    print("Free Stock Images MCP Server - API Integration Demo")
    print("=" * 55)
    
    # Example 1: Try Unsplash API (if configured)
    print("\n🔍 Testing Unsplash API...")
    unsplash_key = os.getenv("UNSPLASH_ACCESS_KEY")
    if unsplash_key:
        print(f"✅ Unsplash API key found: {unsplash_key[:8]}...")
        api_data = make_api_request("unsplash", "sunset", 3)
        if api_data:
            formatted = format_api_results("unsplash", api_data, "sunset")
            print(formatted)
        else:
            print("❌ API request failed")
    else:
        print("❌ No Unsplash API key configured (UNSPLASH_ACCESS_KEY)")
    
    # Example 2: Try Pexels API (if configured)
    print("\n🔍 Testing Pexels API...")
    pexels_key = os.getenv("PEXELS_API_KEY")
    if pexels_key:
        print(f"✅ Pexels API key found: {pexels_key[:8]}...")
        api_data = make_api_request("pexels", "nature", 3)
        if api_data:
            formatted = format_api_results("pexels", api_data, "nature")
            print(formatted)
        else:
            print("❌ API request failed")
    else:
        print("❌ No Pexels API key configured (PEXELS_API_KEY)")
    
    # Example 3: Show fallback behavior
    print("\n🔍 Testing Freepik (no API available)...")
    api_data = make_api_request("freepik", "business", 3)
    if api_data:
        print("✅ Got API data")
    else:
        print("❌ No API available - will use web search fallback")
    
    print("\n" + "=" * 55)
    print("Configuration Instructions:")
    print("export UNSPLASH_ACCESS_KEY=your_key_here")
    print("export PEXELS_API_KEY=your_key_here")  
    print("export PIXABAY_API_KEY=your_key_here")
    print("\nGet API keys from:")
    print("- Unsplash: https://unsplash.com/developers")
    print("- Pexels: https://www.pexels.com/api/")
    print("- Pixabay: https://pixabay.com/api/docs/")

if __name__ == "__main__":
    demo_api_integration()