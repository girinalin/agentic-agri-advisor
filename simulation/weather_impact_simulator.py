import random


class WeatherImpactSimulator:
    def __init__(self):
        self.current_temp = 20.0
        self.current_humidity = 60.0
        self.current_rain = 0.0
        self.day = 0

    def step(self):
        self.day += 1
        base_temp = 22.0 + 4.0 * (self.day / 30.0)
        self.current_temp = base_temp + random.uniform(-3.0, 3.0)
        self.current_humidity = max(20.0, min(95.0, 60.0 + random.uniform(-15.0, 15.0)))

        if self.current_humidity > 80.0 and random.random() > 0.4:
            self.current_rain = random.uniform(5.0, 25.0)
        else:
            self.current_rain = 0.0

        anomalies = []
        if self.current_temp < 5.0:
            anomalies.append("frost_risk")
        if self.current_temp > 35.0:
            anomalies.append("heatwave")

        return {
            "temp_c": round(self.current_temp, 1),
            "humidity": round(self.current_humidity, 1),
            "rain_mm": round(self.current_rain, 1),
            "anomalies": anomalies,
        }
