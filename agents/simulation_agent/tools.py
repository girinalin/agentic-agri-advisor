import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../simulation")))

from env import FarmSimulationEnv

env_session = None


def start_new_simulation(crop_type: str = "corn") -> str:
    """Initialize a new farm simulation session.

    Args:
        crop_type: Type of crop to grow (corn, wheat, etc.).
    """
    global env_session
    env_session = FarmSimulationEnv(crop_type)
    return f"New farm simulation env initialized for crop '{crop_type}'."


def step_farm_simulation(days: int = 1, irrigation_liters: float = 0.0, treatment_applied: bool = False) -> dict:
    """Advance the farm simulation loop by N days with optional input actions.

    Args:
        days: Number of days to run step loop.
        irrigation_liters: Volume of water applied per day.
        treatment_applied: Whether pest/disease spray is applied.
    """
    global env_session
    if env_session is None:
        env_session = FarmSimulationEnv("corn")
        
    latest_state = {}
    for _ in range(days):
        latest_state = env_session.step({
            "irrigation_liters": irrigation_liters,
            "treatment_applied": treatment_applied
        })
        
    return {
        "status": "success",
        "current_day": len(env_session.history),
        "latest_daily_state": latest_state,
        "history_summary": [
            {
                "day": h["day"],
                "health": h["crop"]["health"],
                "moisture": h["soil"]["soil_moisture"],
                "pest_index": h["pest"]["pest_index"],
                "price": h["market"]["price_usd"]
            }
            for h in env_session.history
        ]
    }
