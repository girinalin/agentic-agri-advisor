import random
import os
import json

class MarketPriceSimulator:
    def __init__(self, commodity="corn"):
        self.commodity = commodity.lower().strip()
        self.base_price = 4.50 if self.commodity == "corn" else 6.12
        
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            params_path = os.path.join(current_dir, "historical_parameters.json")
            if os.path.exists(params_path):
                with open(params_path, "r") as f:
                    params = json.load(f)
                prices = params.get("commodity_base_prices_usd", {})
                if self.commodity in prices:
                    self.base_price = prices[self.commodity]
        except Exception:
            pass
            
        self.current_price = self.base_price

    def step(self, regional_yield_health):
        health_factor = 1.0 - (regional_yield_health / 100.0)
        scarcity_premium = health_factor * 0.50
        
        fluctuation = random.uniform(-0.05, 0.05)
        self.current_price = round(self.base_price + scarcity_premium + fluctuation, 2)
        return {
            "price_usd": self.current_price
        }
