# How to Search ak-vrana.cz for "odcizeni"

This document demonstrates how to use the MCP server to search for "odcizeni" on ak-vrana.cz.

## Method 1: Using the MCP Server (Recommended)

### Step 1: Start the MCP Server

```bash
# Using Docker
docker run -p 8000:8000 judicature-mcp

# Or directly with Python
python server.py
```

The server will start on `http://localhost:8000`.

### Step 2: Connect with an MCP Client

The server implements the Model Context Protocol (MCP) and can be accessed by any MCP client (like Claude Desktop, or other MCP-compatible tools).

### Step 3: Call the search_ak_vrana Tool

Use the MCP client to call the `search_ak_vrana` tool with the following parameters:

```json
{
  "name": "search_ak_vrana",
  "arguments": {
    "keywords": "odcizeni"
  }
}
```

### Expected Response

The tool will return a JSON response containing search results:

```json
{
  "query": "odcizeni",
  "url": "https://ak-vrana.cz/?s=odcizeni",
  "total_articles": 10,
  "total_links": 45,
  "articles": [
    {
      "text": "Odcizení věci - právní rozbor",
      "link": "https://ak-vrana.cz/odcizeni-veci/"
    },
    ...
  ]
}
```

## Method 2: Using the Demo Script

For testing purposes, we've included a standalone demo script:

```bash
python demo_search.py
```

This will demonstrate the search functionality by searching for "odcizeni" and displaying the results.

## Method 3: Direct API Call (if using HTTP mode)

If the server is running in HTTP mode, you can make direct HTTP requests to the MCP endpoints.

## What the Tool Does

The `search_ak_vrana` tool:

1. Takes a keyword (in this case "odcizeni")
2. Constructs a search URL: `https://ak-vrana.cz/?s=odcizeni`
3. Fetches the search results page
4. Parses the HTML to extract article information
5. Returns a structured JSON response with:
   - The search query
   - The URL that was searched
   - Total number of articles found
   - Total number of links found
   - An array of articles with their titles and links

## Example Use Cases

1. **Legal Research**: Search for specific legal terms in Czech case law
2. **Case Discovery**: Find relevant cases about theft ("odcizeni")
3. **Content Extraction**: Use the results with `extract_page_content` to get full article text

## Troubleshooting

- Ensure the server is running before making requests
- Check network connectivity to ak-vrana.cz
- Verify the MCP client is properly configured to connect to the server
