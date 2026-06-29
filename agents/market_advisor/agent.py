from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from agents.dashboard_agent.tools import refresh_market_schema, get_ui_schema

market_advisor_agent = Agent(
    name="market_advisor_agent",
    model=Gemini(
        model="gemini-3.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are an agricultural economist. Your task is to track local and global crop commodity "
        "prices, analyze market supply and demand trends, and advise on optimal harvest selling times. "
        "If the user asks for current crop prices, market insights, or commodity rates, you MUST "
        "execute the 'refresh_market_schema' tool first to retrieve the live futures pricing, "
        "then you MUST execute the 'get_ui_schema' tool with 'market_insights' as input and output the raw "
        "JSON block in your response so the client can render it."
    ),
    tools=[refresh_market_schema, get_ui_schema],
)


