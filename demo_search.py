#!/usr/bin/env python3
"""
Demo script showing how to use the search_ak_vrana tool.

This demonstrates searching for "odcizeni" on the ak-vrana.cz website.
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the functions directly
import requests
from bs4 import BeautifulSoup
import json


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


if __name__ == "__main__":
    print("=" * 70)
    print("MCP Caselaw Server Demo: Searching ak-vrana.cz for 'odcizeni'")
    print("=" * 70)
    print()
    
    # Example 1: Search for "odcizeni"
    print("Example 1: Searching for 'odcizeni'")
    print("-" * 70)
    result = search_ak_vrana("odcizeni")
    print(result)
    print()
    
    # Parse and display summary
    result_data = json.loads(result)
    if "error" not in result_data:
        print(f"✓ Search successful!")
        print(f"  - Query: {result_data.get('query')}")
        print(f"  - URL: {result_data.get('url')}")
        print(f"  - Total articles found: {result_data.get('total_articles')}")
        print(f"  - Total links found: {result_data.get('total_links')}")
        if result_data.get('articles'):
            print(f"  - First result: {result_data['articles'][0].get('text')}")
    else:
        print(f"✗ Search failed: {result_data.get('error')}")
    
    print()
    print("=" * 70)
    print("Note: This demonstrates the search_ak_vrana tool functionality.")
    print("In a real MCP client, you would call this tool via the MCP protocol.")
    print("=" * 70)
