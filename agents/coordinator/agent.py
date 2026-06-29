from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

# Import specialist agents
from agents.crop_analyst.agent import crop_analyst_agent
from agents.weather_advisor.agent import weather_advisor_agent
from agents.market_advisor.agent import market_advisor_agent
from agents.pest_detector.agent import pest_detector_agent
from agents.irrigation_advisor.agent import irrigation_advisor_agent
from agents.farmer_interaction.agent import farmer_interaction_agent
from agents.knowledge_retriever.agent import knowledge_retriever_agent
from agents.simulation_agent.agent import simulation_agent
from agents.dashboard_agent.agent import dashboard_agent
from agents.dashboard_agent.tools import get_ui_schema

# Coordinator agent that delegates queries to the specialized advisors
coordinator_agent = Agent(
    name="coordinator_agent",
    model=Gemini(
        model="gemini-3.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are the main coordinator for the Agentic Agriculture Advisor (AAA). "
        "Your role is to triage the farmer's query and coordinate with specialized sub-agents. "
        "CRITICAL: If the user asks to show, open, display, or layout any UI dashboard, planner, "
        "alert card, insights, simulator sandbox, or voice assistant controller, you MUST "
        "execute the 'get_ui_schema' tool with the corresponding schema name: "
        "'crop_dashboard', 'irrigation_planner', 'pest_alert', 'market_insights', 'simulation', "
        "or 'voice_interface'. You must output the exact returned JSON block inside a markdown code block "
        "in your final response so the client can parse and render the wizard inline."
    ),
    sub_agents=[
        crop_analyst_agent,
        weather_advisor_agent,
        market_advisor_agent,
        pest_detector_agent,
        irrigation_advisor_agent,
        farmer_interaction_agent,
        knowledge_retriever_agent,
        simulation_agent(),
        dashboard_agent()
    ],
    tools=[get_ui_schema],
)

