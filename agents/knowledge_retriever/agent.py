from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

# Declared MCP Tools: retrieve_agronomy_documents, query_knowledge_graph

knowledge_retriever_agent = Agent(
    name="knowledge_retriever_agent",
    model=Gemini(
        model="gemini-3.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="You are a database and manual retriever. Retrieve relevant knowledge logs from RAG and OKF.",
    tools=[],
)
