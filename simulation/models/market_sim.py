# Placeholder for crop commodity market price simulators (random walk)
import random


class CommodityMarketSimulator:
    def __init__(self, volatility: float = 0.02):
        self.volatility = volatility

    def update_price(self, current_price: float) -> float:
        """Calculate next day's price using a basic random walk model."""
        change = current_price * random.normalvariate(0, self.volatility)
        return max(0.50, current_price + change)
