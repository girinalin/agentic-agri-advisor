# Placeholder for coordinator-specific tools
from google.adk.tools import ToolContext

def routing_helper(query: str, tool_context: ToolContext) -> dict:
    """Helper tool to assist in routing decision logs.

    Args:
        query: The raw query string to categorize.

    Returns:
        dict: A categorization dictionary.
    """
    return {"status": "success", "category": "uncategorized"}
