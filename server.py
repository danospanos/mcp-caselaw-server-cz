"""
FastMCP Server - HTTP/ASGI mode with Uvicorn
"""
from fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import json

# Create FastMCP instance
mcp = FastMCP("Judicature MCP Server")


@mcp.tool()
def search_ak_vrana(keywords: str) -> str:
    """
    Search the ak-vrana.cz website for articles matching the given keywords.
    
    Args:
        keywords: Search keywords (e.g., "odcizeni veci")
    
    Returns:
        JSON string containing a list of articles with their titles and links
    """
    # Convert keywords to URL format (replace spaces with +)
    search_query = keywords.replace(" ", "+")
    url = f"https://ak-vrana.cz/?s={search_query}"
    
    try:
        # Fetch the page
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the main element
        main = soup.find('main')
        
        if not main:
            return json.dumps({"error": "No main element found on the page", "articles": []})
        
        # Find all articles within main
        articles = main.find_all('article')
        
        results = []
        for article in articles:
            # Find all links within the article
            links = article.find_all('a')
            
            for link in links:
                # Extract text and href
                text = link.get_text(strip=True)
                href = link.get('href', '')
                
                # Only add if both text and href exist
                if text and href:
                    results.append({
                        "text": text,
                        "link": href
                    })
        
        return json.dumps({
            "query": keywords,
            "url": url,
            "total_articles": len(articles),
            "total_links": len(results),
            "articles": results
        }, ensure_ascii=False, indent=2)
        
    except requests.RequestException as e:
        return json.dumps({
            "error": f"Request failed: {str(e)}",
            "query": keywords,
            "url": url,
            "articles": []
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "error": f"Parsing failed: {str(e)}",
            "query": keywords,
            "url": url,
            "articles": []
        }, ensure_ascii=False, indent=2)

@mcp.tool()
def extract_page_content(url: str) -> str:
    """
    Extract and convert the main content of a webpage to Markdown format.
    
    This tool fetches a webpage, extracts the HTML content within the <main> element,
    and converts it to clean Markdown text suitable for LLM processing.
    
    Args:
        url: The full URL of the webpage to extract content from
    
    Returns:
        JSON string containing the URL, markdown content, and any errors
    """
    try:
        # Fetch the page
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the main element
        main = soup.find('main')
        
        if not main:
            return json.dumps({
                "url": url,
                "error": "No <main> element found on the page",
                "markdown": ""
            }, ensure_ascii=False, indent=2)
        
        # Convert the main content to markdown
        markdown_content = md(str(main), heading_style="ATX", strip=['script', 'style'])
        
        return json.dumps({
            "url": url,
            "markdown": markdown_content,
            "character_count": len(markdown_content),
            "success": True
        }, ensure_ascii=False, indent=2)
        
    except requests.RequestException as e:
        return json.dumps({
            "url": url,
            "error": f"Request failed: {str(e)}",
            "markdown": ""
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "url": url,
            "error": f"Processing failed: {str(e)}",
            "markdown": ""
        }, ensure_ascii=False, indent=2)

# Create ASGI app for HTTP serving
app = mcp.http_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
