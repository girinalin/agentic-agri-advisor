from google.adk.agents import Agent

from agents.dashboard_agent.tools import get_ui_schema

from . import tools


def simulation_agent() -> Agent:
    """Creates the Simulation Agent."""
    agent = Agent(
        name="simulation_agent",
        instruction=(
            "Manages Gym-style farm simulation runs and daily crop forecast updates. "
            "If asked to show, open, display, or update the simulation sandbox or simulator interface, "
            "you MUST execute the 'get_ui_schema' tool with 'simulation' as input and output the raw JSON block in your final response."
        ),
    )
    agent.tools = [
        tools.start_new_simulation,
        tools.step_farm_simulation,
        get_ui_schema,
    ]
    return agent
