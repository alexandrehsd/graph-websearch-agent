def format_results(organic_results):
    result_strings = []
    for result in organic_results:
        title = result.get("title", "No Title")
        link = result.get("link", "#")
        snippet = result.get("snippet", "No snippet available")
        result_strings.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n---")
    
    return "\n".join(result_strings)


def is_garbled(text):
    """
    A simple heuristic to detect garbled text:
    high proportion of non-ASCII characters
    """
    non_ascii_count = sum(1 for char in text if ord(char) > 127)
    return non_ascii_count > len(text) * 0.3