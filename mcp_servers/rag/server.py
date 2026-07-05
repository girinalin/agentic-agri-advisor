import os
import sys

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Agronomy-RAG-Retriever")

current_dir = os.path.dirname(os.path.abspath(__file__))
retriever_path = os.path.join(current_dir, "../../rag_pipeline/retriever")
sys.path.append(retriever_path)


@mcp.tool()
async def retrieve_agronomy_documents(query: str, top_k: int = 3) -> list[dict]:
    """Search agricultural and crop manuals for relevant context.

    Args:
        query: Search string or question.
        top_k: Number of documents to retrieve.
    """
    try:
        from search import search

        results = search(query, top_k)
        return results
    except Exception as e:
        return [
            {
                "error": str(e),
                "note": "Make sure search.py is accessible and index exists",
            }
        ]
