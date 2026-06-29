from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from agents.dashboard_agent.tools import get_ui_schema

irrigation_advisor_agent = Agent(
    name="irrigation_advisor_agent",
    model=Gemini(
        model="gemini-3.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are an expert irrigation optimizer. Recommend water schedules based on crop, weather, and soil inputs. "
        "If asked to show, open, display, or update the irrigation planner, you MUST "
        "execute the 'get_ui_schema' tool with 'irrigation_planner' as input and output the raw JSON block in your final response."
    ),
    tools=[get_ui_schema],
)

