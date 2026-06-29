class IrrigationSimulator:
    def __init__(self):
        self.soil_moisture = 40.0

    def step(self, rain_mm, irrigation_liters):
        depletion = 2.5
        moisture_gain = (rain_mm * 1.5) + (irrigation_liters * 0.8)
        self.soil_moisture = max(0.0, min(100.0, self.soil_moisture - depletion + moisture_gain))
        return {
            "soil_moisture": round(self.soil_moisture, 1)
        }
