# Placeholder for weather forecast and condition simulators
import random


class WeatherSimulator:
    def __init__(self, rain_probability: float = 0.15):
        self.rain_probability = rain_probability

    def generate_daily_weather(self) -> dict:
        """Simulate temperature (Celsius) and precipitation (mm)."""
        is_raining = random.random() < self.rain_probability
        return {
            "temp_c": random.uniform(15.0, 32.0),
            "precip_mm": random.uniform(5.0, 25.0) if is_raining else 0.0,
            "condition": "rainy" if is_raining else "sunny",
        }
