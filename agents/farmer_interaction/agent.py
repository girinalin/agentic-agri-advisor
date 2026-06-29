from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from agents.dashboard_agent.tools import get_ui_schema

farmer_interaction_agent = Agent(
    name="farmer_interaction_agent",
    model=Gemini(
        model="gemini-3.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are a multilingual voice interaction interface. Convert speech to text and format vocal advisor responses in English, Spanish, and Swahili. "
        "If asked to show, open, display, or update the voice control interface or microphone tool, you MUST "
        "execute the 'get_ui_schema' tool with 'voice_interface' as input and output the raw JSON block in your final response."
    ),
    tools=[get_ui_schema],
)

