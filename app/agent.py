import os

from dotenv import find_dotenv, load_dotenv
from google.adk.apps import App

# Load local environment variables when running from source.
load_dotenv(find_dotenv(usecwd=True), override=False)

# Setup environment for Vertex AI or Gemini Developer API (AI Studio)
if "GEMINI_API_KEY" in os.environ and not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

if "GOOGLE_API_KEY" in os.environ:
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
else:
    try:
        import google.auth
        _, project_id = google.auth.default()
        os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
        os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
    except Exception:
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

# Import our actual agricultural coordinator agent
from agents.coordinator.agent import coordinator_agent

root_agent = coordinator_agent

app = App(
    root_agent=coordinator_agent,
    name="app",
)

