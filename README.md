# Judicature MCP

FastMCP server running over HTTP with Uvicorn.

## Available Tools

### 1. `search_ak_vrana`
Search the ak-vrana.cz website for articles matching given keywords.

**Parameters:**
- `keywords` (string): Search keywords (e.g., "odcizeni veci")

**Returns:** JSON with search results including article links and text.

### 2. `extract_page_content`
Extract and convert webpage content to Markdown format.

**Parameters:**
- `url` (string): Full URL of the webpage to extract

**Returns:** JSON with markdown-formatted content from the page's `<main>` element.

## Quick Start

**Build:**
```bash
docker build -t judicature-mcp .
```

**Run:**
```bash
docker run -p 8000:8000 judicature-mcp
```

**Access:** http://localhost:8000

## Usage Examples

### Search for "odcizeni"
The server provides a `search_ak_vrana` tool that can search for any keywords. For example, to search for "odcizeni":

**Using an MCP client:**
```json
{
  "tool": "search_ak_vrana",
  "arguments": {
    "keywords": "odcizeni"
  }
}
```

**Using the demo script:**
```bash
python demo_search.py
```

**Using the verification script:**
```bash
python verify_tools.py
```

For detailed instructions, see [SEARCH_GUIDE.md](SEARCH_GUIDE.md).

## Development

**With auto-reload:**
```bash
docker run -p 8000:8000 -v $(pwd):/app judicature-mcp uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

**Interactive shell:**
```bash
docker run -it --rm judicature-mcp /bin/bash
```

## Known Issues

- **Search pagination**: The `search_ak_vrana` tool only processes the first page of search results. If the search returns multiple pages, subsequent pages are not retrieved.
- **Extra content in extraction**: The `extract_page_content` tool extracts all content within `<main>` tags, which may include crossroad/navigation elements below the main article text, potentially causing unintended text additions in the markdown output.
