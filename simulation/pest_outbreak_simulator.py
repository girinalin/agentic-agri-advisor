import random


class PestOutbreakSimulator:
    def __init__(self):
        self.pest_index = 5.0

    def step(self, humidity, treatment_applied=False):
        if treatment_applied:
            self.pest_index = max(1.0, self.pest_index - random.uniform(15.0, 25.0))
        else:
            growth_rate = 1.0
            if humidity > 80.0:
                growth_rate = 3.5
            self.pest_index = min(
                100.0, self.pest_index + random.uniform(0.5, growth_rate)
            )

        outbreak = "critical" if self.pest_index > 40.0 else "normal"
        return {"pest_index": round(self.pest_index, 1), "outbreak_status": outbreak}
