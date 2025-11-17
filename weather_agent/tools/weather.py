import requests
import os

def get_weather(location: str):
    """
    Fetches weather information for a given city using wttr.in.
    """
    url = f"{os.getenv('WEATHER_API_URL')}/{location}?format=j1"

    response = requests.get(url)
    data = response.json()

    return {
        "location": location,
        "temperature_c": data["current_condition"][0]["temp_C"],
        "description": data["current_condition"][0]["weatherDesc"][0]["value"]
    }
