import openmeteo_requests
import requests_cache
import numpy as np

def fetch_live_weather(lat, lon):
    session = requests_cache.CachedSession('.cache', expire_after=3600)
    openmeteo = openmeteo_requests.Client(session=session)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "timezone": "auto"
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()
    temperature = hourly.Variables(0).ValuesAsNumpy()
    return {"temperature": temperature.tolist()}

def simulate_cyclone(lat, lon, radius):
    # Simulate a cyclone by generating random weather data
    cyclone_data = {
        "lat": lat,
        "lon": lon,
        "radius": radius,
        "intensity": np.random.uniform(0.5, 1.0),
    }
    return cyclone_data