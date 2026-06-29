import os
import json

class CropGrowthSimulator:
    def __init__(self, crop_type="corn"):
        self.crop_type = crop_type.lower()
        self.stage = "germination"
        self.growth_index = 0.0
        self.biomass = 0.0
        self.health = 100.0
        self.days_planted = 0
        
        self.historical_yield_target = 5.0
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            params_path = os.path.join(current_dir, "historical_parameters.json")
            if os.path.exists(params_path):
                with open(params_path, "r") as f:
                    params = json.load(f)
                crop_yields = params.get("crop_yield_ton_ha", {})
                if self.crop_type in crop_yields:
                    self.historical_yield_target = crop_yields[self.crop_type].get("historical_yield_ton_ha", 5.0)
        except Exception:
            pass

    def step(self, temp, water_level, pest_level):
        self.days_planted += 1
        
        temp_factor = 1.0 - abs(temp - 23.0) / 15.0
        temp_factor = max(0.1, min(1.0, temp_factor))
        
        water_factor = 1.0 - abs(water_level - 50.0) / 40.0
        water_factor = max(0.1, min(1.0, water_factor))
        
        pest_factor = max(0.1, 1.0 - (pest_level / 100.0))
        
        daily_growth = 1.5 * temp_factor * water_factor * pest_factor
        self.growth_index = min(100.0, self.growth_index + daily_growth)
        
        if water_level < 15.0 or water_level > 85.0:
            self.health = max(0.0, self.health - 2.0)
        if pest_level > 30.0:
            self.health = max(0.0, self.health - (pest_level * 0.1))
        else:
            self.health = min(100.0, self.health + 0.5)

        if self.stage == "vegetative":
            self.biomass += 0.2 * temp_factor * pest_factor
        elif self.stage == "flowering":
            self.biomass += 0.5 * temp_factor * pest_factor
        elif self.stage == "maturity":
            self.biomass += 0.8 * temp_factor * pest_factor
            
        if self.growth_index >= 100.0:
            self.stage = "harvested"
        elif self.growth_index >= 75.0:
            self.stage = "maturity"
        elif self.growth_index >= 40.0:
            self.stage = "flowering"
        elif self.growth_index >= 15.0:
            self.stage = "vegetative"
            
        return {
            "stage": self.stage,
            "growth_index": round(self.growth_index, 1),
            "biomass_kg": round(self.biomass, 1),
            "health": round(self.health, 1)
        }
