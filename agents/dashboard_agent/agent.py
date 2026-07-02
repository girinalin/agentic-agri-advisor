from google.adk.agents import Agent

from . import tools


def dashboard_agent() -> Agent:
    """Creates the A2UI Dashboard Agent."""
    agent = Agent(
        name="dashboard_agent",
        instruction=(
            "You are the dashboard agent. Your job is to fetch UI schemas and update dashboard states. "
            "When asked to open, show, or display a specific dashboard, planner, sandbox, or interface, "
            "you MUST execute the 'get_ui_schema' tool for that component (e.g. 'crop_dashboard', "
            "'irrigation_planner', 'market_insights', 'pest_alert', 'simulation', 'voice_interface') "
            "and output the raw JSON payload in your final response so the client can render it."
        )
    )
    agent.tools = [tools.refresh_market_schema, tools.refresh_crop_schema, tools.get_ui_schema, tools.get_local_mandi_prices]
    return agent
