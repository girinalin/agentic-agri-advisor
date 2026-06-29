# Farm Simulation Environment

This sandbox models agricultural conditions—including crop growth, weather fluctuations, and market commodity prices—allowing agents to test crop recommendations and schedules.

## Folder Structure

* `config.yaml`: Configuration parameter values for simulation rules.
* `env.py`: The simulated environment class (similar to OpenAI Gym structure).
* `models/crop_growth.py`: Dynamic mathematical model representing crop yields under different conditions.
* `models/weather_sim.py`: Stochastic simulation of temperature, rain, and frost.
* `models/market_sim.py`: Price dynamics simulation for commodities.
* `run_simulation.py`: Entry point runner script.
