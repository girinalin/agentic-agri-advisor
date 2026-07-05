# Tools for irrigation optimization


def calculate_irrigation_demand(
    crop: str, soil_moisture: float, weather_temp: float
) -> dict:
    """Calculate required water volume (liters/acre) based on crop and current metrics.

    Args:
        crop: Name of the crop (e.g. corn, wheat).
        soil_moisture: Percentage of current soil moisture.
        weather_temp: Current temperature in Celsius.

    Returns:
        dict: Irrigation recommendation.
    """
    return {
        "status": "success",
        "irrigate_liters": 1500.0 if soil_moisture < 20 else 0.0,
    }
