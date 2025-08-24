# Free Stock Images MCP Server

A Model Context Protocol (MCP) server that provides access to multiple free
stock image sources including Unsplash, Pexels, Pixabay, Freepik, Burst, and
StockVault. 

## Features

- 🎨 **Multiple Sources**: Access 6 popular free stock image platforms
- 🔍 **Smart Search**: Search across all sources with a single query
- 🔗 **Direct Links**: Get direct URLs to browse and download images  
- 📋 **License Info**: Guidance on checking license requirements
- 🚀 **Fast & Simple**: Lightweight server with minimal dependencies
- 🔒 **Type Safe**: Comprehensive type hints with TypedDict for better development experience
- 🔌 **API Integration**: Uses `requests` library for real API calls when API keys are configured
- ⚡ **Smart Fallback**: Falls back to web search links when APIs are unavailable

## Supported Stock Image Sources

| Source         | Description                               | License Type     |
| -------------- | ----------------------------------------- | ---------------- |
| **Unsplash**   | Beautiful free photos & images            | Unsplash License |
| **Pexels**     | Free stock photos & royalty free images   | Pexels License   |
| **Pixabay**    | Stunning royalty-free images & stock      | Pixabay License  |
| **Freepik**    | Free vectors, stock photos, PSD and icons | Freepik License  |
| **Burst**      | Free stock photos for commercial use      | CC0              |
| **StockVault** | Free graphics and photos                  | Various          |

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/free-stock-images-mcp.git
cd free-stock-images-mcp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage with Claude Desktop

1. Add to your Claude Desktop config file:

**On macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**On Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "free-stock-images": {
      "command": "python",
      "args": ["/path/to/free-stock-images-mcp/src/server.py"]
    }
  }
}
```

2. Restart Claude Desktop

### Usage with Other MCP Clients

Run the server directly:

```bash
python src/server.py
```

## API Configuration (Optional)

For enhanced functionality with actual image data, configure API keys:

```bash
# Unsplash API (https://unsplash.com/developers)
export UNSPLASH_ACCESS_KEY=your_access_key_here

# Pexels API (https://www.pexels.com/api/)  
export PEXELS_API_KEY=your_api_key_here

# Pixabay API (https://pixabay.com/api/docs/)
export PIXABAY_API_KEY=your_api_key_here
```

**Benefits of API Configuration:**
- Get actual image URLs and metadata
- Access image dimensions, author info, and download links
- Faster, more structured results
- Higher quality search results

**Without API keys:** Falls back to web search links (still fully functional!)

## Available Tools

### 1. `search_stock_images`

Search for stock images across multiple sources.

**Parameters:**

- `query` (required): Search term (e.g., "sunset", "business meeting")
- `sources` (optional): Array of source IDs to search (default: all sources)
- `limit` (optional): Max results per source (default: 5, max: 20)

**Example:**

```json
{
  "query": "mountain landscape",
  "sources": ["unsplash", "pexels", "pixabay"],
  "limit": 3
}
```

### 2. `get_stock_image_sources`

Get information about available stock image sources.

### 3. `check_api_status`

Check the configuration status of API keys for all sources. Shows which APIs are properly configured and provides setup instructions.

**Example API Status Output:**

```text
# API Configuration Status

## Unsplash
✅ **API Endpoint:** https://api.unsplash.com/search/photos
✅ **API Key (UNSPLASH_ACCESS_KEY):** Configured (abc12345...)

## Pexels  
✅ **API Endpoint:** https://api.pexels.com/v1/search
❌ **API Key (PEXELS_API_KEY):** Not found in environment

## Freepik
❌ **API Status:** No public API available
🔗 **Fallback:** Web search links only
```

## Available Resources

Access information about stock image sources:

- `stock-images://unsplash` - Unsplash information
- `stock-images://pexels` - Pexels information
- `stock-images://pixabay` - Pixabay information
- `stock-images://freepik` - Freepik information
- `stock-images://burst` - Burst information
- `stock-images://stockvault` - StockVault information

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/your-username/free-stock-images-mcp.git
cd free-stock-images-mcp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install -e .
```

### Project Structure

```
free-stock-images-mcp/
├── src/
│   ├── __init__.py        # Package initialization
│   ├── server.py          # Main MCP server with requests-based API integration
│   └── types.py           # Type definitions (TypedDict classes)
├── requirements.txt       # Python dependencies (requests, mcp, pydantic)
├── pyproject.toml        # Project configuration
├── test_server.py        # Test script
├── example_usage.py      # Usage examples
├── README.md             # This file
├── LICENSE               # MIT License
└── .gitignore           # Git ignore rules
```

### Adding New Stock Image Sources

1. Add the new source to `STOCK_IMAGE_SOURCES` in `server.py`:

```python
STOCK_IMAGE_SOURCES = {
    # ... existing sources ...
    "newsource": {
        "name": "New Source",
        "base_url": "https://newsource.com/search/",
        "description": "Description of new source"
    }
}
```

2. Test the integration
3. Update the README documentation

### Testing

```bash
# Run the server directly for testing
python src/server.py

# Test with MCP inspector (if available)  
npx @modelcontextprotocol/inspector python src/server.py

# Run the test suite
python test_server.py

# Run usage examples
python example_usage.py
```

## License Requirements

⚠️ **Important**: Always check the license requirements for each stock image source:

- **Unsplash**: Generally free for commercial and personal use, attribution appreciated
- **Pexels**: Free for commercial and personal use, attribution not required but appreciated
- **Pixabay**: Free for commercial and personal use under Pixabay License
- **Freepik**: Free with attribution required, or premium license available
- **Burst**: CC0 license - completely free for any use
- **StockVault**: Various licenses - check individual image licensing

Always verify the current license terms on each platform before using images in your projects.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make changes and test thoroughly
4. Commit with clear messages: `git commit -m "Add new stock image source"`
5. Push to branch: `git push origin feature/new-feature`
6. Create a Pull Request

## Troubleshooting

### Common Issues

**Q: "Module 'mcp' not found"**
A: Install the MCP package: `pip install mcp`

**Q: "Server not responding in Claude Desktop"**
A: Check that the path in `claude_desktop_config.json` is absolute and correct

**Q: "No results returned"**
A: Verify your internet connection and try a different search query

**Q: "Permission denied"**
A: Ensure the server script has execute permissions: `chmod +x src/server.py`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with the [Model Context Protocol](https://modelcontextprotocol.io/)
- Thanks to all the free stock image platforms for providing amazing content
- Inspired by the MCP community and examples
