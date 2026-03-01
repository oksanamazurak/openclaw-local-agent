from langchain_core.tools import tool


@tool
def internet_search(query: str) -> str:
    """Search the internet for the given query and return a summary of results.

    Use this when the user asks about current events, weather, news, or anything
    that requires up-to-date information from the web.
    """
    try:
        from ddgs import DDGS

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))

        if not results:
            return f"No results found for: {query}"

        lines = []
        for i, r in enumerate(results, 1):
            title = r.get("title", "")
            body = r.get("body", "")
            href = r.get("href", "")
            lines.append(f"{i}. **{title}**\n   {body}\n   Source: {href}")

        return "\n\n".join(lines)

    except ImportError:
        return "Error: ddgs package is not installed. Run: pip install ddgs"
    except Exception as e:
        return f"Search error: {e}"
