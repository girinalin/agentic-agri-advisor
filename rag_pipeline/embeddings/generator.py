import json
import os

import yaml
from google import genai


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    words = text.split()
    if not words:
        return []
    for i in range(0, len(words), max(1, chunk_size - overlap)):
        chunk = " ".join(words[i : i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks


def generate_embeddings():
    # Read config
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "../config.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)

    base_raw = os.path.join(current_dir, "../documents/raw")
    index_dir = os.path.join(current_dir, "index")
    index_path = os.path.join(index_dir, "agriculture_index.json")

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

    db = []

    print("Starting RAG Ingestion with Gemini Embeddings...")

    if not os.path.exists(base_raw):
        print(f"Error: Raw documents path {base_raw} does not exist.")
        return

    for category_folder in os.listdir(base_raw):
        cat_path = os.path.join(base_raw, category_folder)
        if not os.path.isdir(cat_path):
            continue

        print(f"Processing category: {category_folder}...")
        for filename in os.listdir(cat_path):
            if filename.startswith(".") or filename.endswith(".gitkeep"):
                continue
            file_path = os.path.join(cat_path, filename)

            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                print(f"  Error reading {filename}: {e}")
                continue

            chunks = chunk_text(content, config["chunk_size"], config["chunk_overlap"])

            for idx, chunk in enumerate(chunks):
                print(f"  Embedding chunk {idx + 1}/{len(chunks)} of {filename}...")
                vector = None
                if client:
                    try:
                        # Call Gemini Embeddings API
                        response = client.models.embed_content(
                            model=config["embedding_model"], contents=chunk
                        )
                        # Extract values (list of floats)
                        vector = response.embedding.values
                    except Exception as e:
                        print(f"    Warning: API call failed. Details: {e}")

                if vector is None:
                    # Mock vector fallback
                    placeholder_vector = [0.0] * config.get("vector_dimension", 768)
                    # Put a 1.0 in the vector to make it non-zero
                    placeholder_vector[0] = 1.0
                    db.append(
                        {
                            "category": category_folder,
                            "file": filename,
                            "chunk_index": idx,
                            "text": chunk,
                            "vector": placeholder_vector,
                            "mocked": True,
                        }
                    )
                else:
                    db.append(
                        {
                            "category": category_folder,
                            "file": filename,
                            "chunk_index": idx,
                            "text": chunk,
                            "vector": vector,
                        }
                    )

    # Save embedded chunks database
    os.makedirs(index_dir, exist_ok=True)
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

    print(f"Ingestion complete. Saved {len(db)} embedded chunks to: {index_path}")


if __name__ == "__main__":
    generate_embeddings()
