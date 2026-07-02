from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

from agents.dashboard_agent.tools import get_ui_schema

pest_detector_agent = Agent(
    name="pest_detector_agent",
    model=Gemini(
        model="gemini-3.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are an expert plant pathologist. Diagnose crop health issues and pests, prescribing treatments. "
        "If asked to show, open, display, or update the pest alert dashboard or warning cards, you MUST "
        "execute the 'get_ui_schema' tool with 'pest_alert' as input and output the raw JSON block in your final response."
    ),
    tools=[get_ui_schema],
)

