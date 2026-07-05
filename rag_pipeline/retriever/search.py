import json
import os
import sys

import yaml
from google import genai


def dot_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))


def magnitude(v):
    return sum(x * x for x in v) ** 0.5


def cosine_similarity(v1, v2):
    m1 = magnitude(v1)
    m2 = magnitude(v2)
    if m1 == 0 or m2 == 0:
        return 0.0
    return dot_product(v1, v2) / (m1 * m2)


def search(query_str: str, top_k: int = 3) -> list[dict]:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "../config.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)

    index_path = os.path.join(current_dir, "../embeddings/index/agriculture_index.json")

    if not os.path.exists(index_path):
        print(
            f"Error: Index database {index_path} not found. Please run the generator first."
        )
        return []

    with open(index_path, encoding="utf-8") as f:
        database = json.load(f)

    # Initialize Google GenAI client
    client = None
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    try:
        if api_key:
            client = genai.Client(api_key=api_key)
        else:
            client = genai.Client()
    except Exception as e:
        print(
            f"Warning: Could not initialize Google GenAI Client: {e}. Falling back to mocks."
        )

    query_vector = None
    if client:
        print(f"Generating query embedding for: '{query_str}'...")
        try:
            response = client.models.embed_content(
                model=config["embedding_model"], contents=query_str
            )
            query_vector = response.embedding.values
        except Exception as e:
            print(f"Warning: Embeddings API call failed. Details: {e}")

    if query_vector is None:
        query_vector = [1.0] + [0.0] * (config.get("vector_dimension", 768) - 1)

    # Compute similarities
    results = []
    for item in database:
        sim = cosine_similarity(query_vector, item["vector"])
        results.append(
            {
                "category": item["category"],
                "file": item["file"],
                "chunk_index": item["chunk_index"],
                "text": item["text"],
                "score": sim,
            }
        )

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)

    top_results = results[:top_k]

    print("\n--- Search Results ---")
    for idx, res in enumerate(top_results):
        print(
            f"\n[{idx + 1}] Score: {res['score']:.4f} | Category: {res['category']} | File: {res['file']}"
        )
        print(f"Content: {res['text']}")

    return top_results


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "late blight treatment"
    search(query)
