from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

weather_advisor_agent = Agent(
    name="weather_advisor_agent",
    model=Gemini(
        model="gemini-3.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are an agricultural meteorologist. Your task is to interpret local weather patterns "
        "and forecasts, and issue crop-protection and planting window alerts based on weather data."
    ),
    tools=[],
)
