# Tool Usage Examples

## Example 1: Search for articles

```python
# Search for articles about "odcizeni veci"
result = search_ak_vrana(keywords="odcizeni veci")
```

**Response:**
```json
{
  "query": "odcizeni veci",
  "url": "https://ak-vrana.cz/?s=odcizeni+veci",
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

## Example 2: Extract page content as Markdown

```python
# Extract and convert a specific article to markdown
result = extract_page_content(url="https://ak-vrana.cz/odcizeni-veci/")
```

**Response:**
```json
{
  "url": "https://ak-vrana.cz/odcizeni-veci/",
  "markdown": "# Odcizení věci\n\nPrávní rozbor problematiky...",
  "character_count": 5420,
  "success": true
}
```

## Workflow: Search + Extract

A typical workflow combining both tools:

1. **Search** for relevant articles using `search_ak_vrana`
2. **Extract** full content from specific articles using `extract_page_content`
3. **Process** the markdown content with an LLM for analysis, summarization, or Q&A

This allows an AI agent to:
- Discover relevant legal content
- Extract clean, LLM-friendly text
- Analyze and answer questions about Czech legal cases
