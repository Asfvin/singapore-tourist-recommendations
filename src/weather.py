import requests
import pandas as pd
import datetime
from typing import Union
import json

# List of URLS
AIR_TEMPERATURE_URL = "https://api-open.data.gov.sg/v2/real-time/api/air-temperature"
RAINFALL_URL = "https://api-open.data.gov.sg/v2/real-time/api/rainfall"
POLUTANT_URL = "https://api-open.data.gov.sg/v2/real-time/api/psi"
WEATHER_FORECAST_URL = (
    "https://api-open.data.gov.sg/v2/real-time/api/twenty-four-hr-forecast"
)


def get_current_date_time() -> str:
    """Current date and time in user timezone"""
    today = datetime.datetime.today().strftime("%H:%M:%S")
    return today


def get_current_temp() -> str:
    temp_response = requests.get(AIR_TEMPERATURE_URL)

    temp_data = temp_response.json()

    # We need to either hardcode the stations id or dynamically select them
    # let the station id be S109 for now
    current_temperature = temp_data["data"]["readings"][0]["data"][0]["value"]
    current_timestamp = temp_data["data"]["readings"][0]["timestamp"]

    return current_temperature


def rain_condition(rainfall_amount: Union[float, int]) -> str:
    """Identify rainfall condition based on these predefined conditions
    Light Rain: 0.1-9.9 mm
    Moderate Rain: 10.0-24.9 mm
    Heavy Rain: 25.0-49.9 mm
    Stormy Rain: 50.0-99.9 mm
    Heavy Stormy Rain: 100.0-249.9 mm
     Very Heavy Stormy Rain: ≥250.0 mm
    """
    if rainfall_amount >= 250:
        return "Very Heavy Stormy Rain"
    elif 249.9 >= rainfall_amount >= 100:
        return "Heavy Stormy Rain"
    elif 99.9 >= rainfall_amount >= 50:
        return "Stormy Rain"
    elif 49.9 >= rainfall_amount >= 25:
        return "Heavy Rain"
    elif 24.9 >= rainfall_amount >= 10:
        return "Moderate Rain"
    elif 9.9 >= rainfall_amount >= 0.1:
        return "Light Rain"
    else:
        return "No Rain"


def return_current_rainfall() -> str:
    """Given the current rainfall amount, return the rainfall condition"""
    rainfall_response = requests.get(RAINFALL_URL)

    rainfall_data = rainfall_response.json()

    rainfall_amount = rainfall_data["data"]["readings"][0]["data"][0]["value"]

    return rain_condition(rainfall_amount)


def get_current_pollutant() -> pd.DataFrame:
    """Current state of pollution in singapore"""
    pollutant_response = requests.get(POLUTANT_URL)

    pollutant_data = pollutant_response.json()
    pollutant_state = pd.read_json(
        json.dumps(pollutant_data["data"]["items"][0]["readings"])
    )

    return pollutant_state


def get_weather_forecast() -> str:
    weather_forecast_response = requests.get(WEATHER_FORECAST_URL)

    weather_data = weather_forecast_response.json()

    # Each Region will have different Forecast
    # general_forecasts = weather_data["data"]["records"][0]["general"]
    # general_temp_lower = general_forecasts["temperature"]["low"]
    # general_temp_upper = general_forecasts["temperature"]["high"]
    # general_humidity_lower = general_forecasts["relativeHumidity"]["low"]
    # general_humidity_upper = general_forecasts["relativeHumidity"]["high"]

    # general_forecast_text = general_forecasts["forecast"]["text"]

    temporal_weather = weather_data["data"]["records"][0]["periods"]

    return temporal_weather
