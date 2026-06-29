# Tools for OKF SPARQL and RAG document queries
from google.adk.tools import ToolContext

def search_local_indices(query: str) -> dict:
    """Search local index files for crop and soil facts.

    Args:
        query: Search string.

    Returns:
        dict: Found snippets.
    """
    return {"status": "success", "results": [{"doc": "factsheet.pdf", "text": "Soil pH should be 6.0-6.8."}]}
