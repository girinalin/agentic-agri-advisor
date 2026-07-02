import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crop_growth_simulator import CropGrowthSimulator
from irrigation_simulator import IrrigationSimulator
from market_price_simulator import MarketPriceSimulator
from pest_outbreak_simulator import PestOutbreakSimulator
from weather_impact_simulator import WeatherImpactSimulator


class FarmSimulationEnv:
    def __init__(self, crop_type="corn"):
        self.crop_sim = CropGrowthSimulator(crop_type)
        self.weather_sim = WeatherImpactSimulator()
        self.irrigation_sim = IrrigationSimulator()
        self.pest_sim = PestOutbreakSimulator()
        self.market_sim = MarketPriceSimulator(crop_type)
        self.history = []

    def step(self, action=None):
        action = action or {}
        irrigation_liters = action.get("irrigation_liters", 0.0)
        treatment_applied = action.get("treatment_applied", False)

        weather_state = self.weather_sim.step()
        soil_state = self.irrigation_sim.step(weather_state["rain_mm"], irrigation_liters)
        pest_state = self.pest_sim.step(weather_state["humidity"], treatment_applied)
        crop_state = self.crop_sim.step(weather_state["temp_c"], soil_state["soil_moisture"], pest_state["pest_index"])
        market_state = self.market_sim.step(crop_state["health"])

        state = {
            "day": len(self.history) + 1,
            "weather": weather_state,
            "soil": soil_state,
            "pest": pest_state,
            "crop": crop_state,
            "market": market_state
        }
        self.history.append(state)
        return state

    def reset(self):
        self.crop_sim = CropGrowthSimulator(self.crop_sim.crop_type)
        self.weather_sim = WeatherImpactSimulator()
        self.irrigation_sim = IrrigationSimulator()
        self.pest_sim = PestOutbreakSimulator()
        self.market_sim = MarketPriceSimulator(self.market_sim.commodity)
        self.history = []
        return {"status": "reset"}

if __name__ == "__main__":
    env = FarmSimulationEnv("corn")
    print("Running basic 5-day simulation verification run...")
    for day in range(1, 6):
        res = env.step({"irrigation_liters": 5.0})
        print(f"Day {day}: Crop Stage={res['crop']['stage']} | Health={res['crop']['health']}% | Moisture={res['soil']['soil_moisture']}% | Price=${res['market']['price_usd']}")
