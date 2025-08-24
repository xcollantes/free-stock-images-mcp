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
      "args": ["/path/to/free-stock-images-mcp/free_stock_images_mcp/server.py"]
    }
  }
}
```

2. Restart Claude Desktop

### Usage with Other MCP Clients

Run the server directly:

```bash
python free_stock_images_mcp/server.py
```

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

**Example Output:**

```
# Available Free Stock Image Sources

## Unsplash
**ID:** `unsplash`
**Description:** Beautiful free photos & images
**Base URL:** https://unsplash.com/s/photos/

## Pexels
**ID:** `pexels`
**Description:** Free stock photos & royalty free images
**Base URL:** https://www.pexels.com/search/
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
├── free_stock_images_mcp/
│   ├── __init__.py
│   └── server.py          # Main MCP server implementation
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
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
python free_stock_images_mcp/server.py

# Test with MCP inspector (if available)
npx @modelcontextprotocol/inspector python free_stock_images_mcp/server.py
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
A: Ensure the server script has execute permissions: `chmod +x free_stock_images_mcp/server.py`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with the [Model Context Protocol](https://modelcontextprotocol.io/)
- Thanks to all the free stock image platforms for providing amazing content
- Inspired by the MCP community and examples
