# Agronomy RAG Pipeline

This directory contains the pipeline for chunking agricultural manuals, generating text embeddings, and retrieving top-k contexts for the LLM agents.

## Folder Structure

* `documents/raw/`: Place raw `.pdf`, `.txt`, or `.md` crop manuals here.
* `documents/processed/`: Chunked and cleaned JSON documents ready for embedding.
* `embeddings/generator.py`: Script to generate text embeddings and build vector indexes.
* `embeddings/index/`: Local vector search database files (e.g., FAISS).
* `retriever/search.py`: Core similarity search retriever logic.
