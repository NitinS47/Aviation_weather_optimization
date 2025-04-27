import streamlit as st
import folium
from streamlit_folium import folium_static
import numpy as np
import heapq
from folium.plugins import HeatMap
from geopy.distance import geodesic
from datetime import datetime
import pickle
import pandas as pd
import requests

# OpenWeatherMap API Key
API_KEY = "6c90fe5699df8471dbbb9922b8860c90"

# Load the weather model
with open("weather_model.pkl", "rb") as f:
    weather_model = pickle.load(f)

# List of supported cities
supported_cities = ["Delhi", "Bangalore", "Chennai", "Kolkata", "Pune", "Jaipur", "Hyderabad"]

# Major cities in India + Neighboring Regions
cities = {
    "Delhi": (28.7041, 77.1025),
    "Mumbai": (19.0760, 72.8777),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Hyderabad": (17.3850, 78.4867),
    "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462),
    "Ahmedabad": (23.0225, 72.5714),
    "Pune": (18.5204, 73.8567),
    "Kochi": (9.9312, 76.2673),
    "Darjeeling": (27.0360, 88.2627),
    "Dubai": (25.2048, 55.2708),
    "Visakhapatnam": (17.6868, 83.2185),
    "Thiruvananthapuram": (8.5241, 76.9366),
    "Guwahati": (26.1445, 91.7362),
    "Patna": (25.5941, 85.1376),
}

# Ocean waypoints for better routing over Bay of Bengal & Arabian Sea
waypoints = {
    "Bay of Bengal 1": (15.0, 85.0),
    "Bay of Bengal 2": (18.0, 88.0),
    "Bay of Bengal 3": (21.0, 91.0),
    "Arabian Sea 1": (12.0, 70.0),
    "Arabian Sea 2": (16.0, 72.0),
}

# Combine cities and waypoints
locations = {**cities, **waypoints}

# Flight Paths
flight_paths = {
    "Delhi to Bangalore": ("Delhi", "Bangalore"),
    "Bangalore to Kolkata": ("Bangalore", "Kolkata"),
    "Bangalore to Dubai": ("Bangalore", "Dubai"),
    "Delhi to Kochi": ("Delhi", "Kochi"),
    "Bangalore to Darjeeling": ("Bangalore", "Darjeeling"),
    "Kolkata to Dubai": ("Kolkata", "Dubai"),   
    "Chennai to Ahmedabad": ("Chennai", "Ahmedabad"),
}

# Function to fetch live weather data from OpenWeatherMap
def fetch_live_weather(city):
    """
    Fetches live weather data for a city using OpenWeatherMap API.
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",  # Use metric units for temperature (Celsius)
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "wind_speed": data["wind"]["speed"] * 3.6,  # Convert m/s to km/h
            "wind_direction": data["wind"].get("deg", 0),  # Wind direction in degrees
            "pressure": data["main"]["pressure"],  # Pressure in hPa
            "precipitation": data.get("rain", {}).get("1h", 0),  # Precipitation in mm (last 1 hour)
        }
    else:
        st.error(f"Failed to fetch weather data for {city}. Status code: {response.status_code}")
        return None

# Generate temperature data for heatmap
def generate_temperature_data():
    return [[lat, lon, np.random.uniform(20, 40)] for lat, lon in locations.values()]

# Generate wind data
def generate_wind_data(cyclone_active=False, cyclone=None):
    wind_data = []
    for lat, lon in locations.values():
        if cyclone_active and is_affected(lat, lon, cyclone):
            # Increase wind speed and randomize direction near the cyclone
            wind_speed = np.random.uniform(50, 100)  # High wind speeds
            wind_direction = np.random.uniform(0, 360)
        else:
            wind_speed = np.random.uniform(5, 20)  # Normal wind speeds
            wind_direction = np.random.uniform(0, 360)
        wind_data.append([lat, lon, wind_speed, wind_direction])
    return wind_data

# Generate pressure data for pressure heatmap
def generate_pressure_data(cyclone_active=False, cyclone=None):
    pressure_data = []
    for lat, lon in locations.values():
        if cyclone_active and is_affected(lat, lon, cyclone):
            # Lower pressure near the cyclone
            pressure = np.random.uniform(950, 980)  # Cyclone causes low pressure
        else:
            pressure = np.random.uniform(980, 1050)  # Normal pressure
        pressure_data.append([lat, lon, pressure])
    return pressure_data

# Generate precipitation data
def generate_precipitation_data(cyclone_active=False, cyclone=None):
    precipitation_data = []
    for lat, lon in locations.values():
        if cyclone_active and is_affected(lat, lon, cyclone):
            # Higher precipitation near the cyclone
            precipitation = np.random.uniform(50, 100)  # Heavy rain
        else:
            precipitation = np.random.uniform(0, 10)  # Light rain
        precipitation_data.append([lat, lon, precipitation])
    return precipitation_data

# Cyclone simulation
def simulate_cyclone():
    return {"lat": 20.0, "lon": 80.0, "radius": 5.0}

# Check if a city is affected by the cyclone
def is_affected(lat, lon, cyclone):
    return geodesic((lat, lon), (cyclone["lat"], cyclone["lon"])).km <= (cyclone["radius"] * 111)

# Weather prediction based on user input
def predict_weather(city, date, time, cyclone_active=False, cyclone=None):
    """
    Predicts weather for a city using the model or OpenWeatherMap API.
    If cyclone is active and the city is affected, returns cyclone-affected weather.
    Otherwise, returns live weather or simulated data.
    """
    if cyclone_active and is_affected(cities[city][0], cities[city][1], cyclone):
        # Cyclone-affected weather
        return {
            "temperature": np.random.uniform(20, 30),
            "wind_speed": np.random.uniform(50, 100),
            "wind_direction": np.random.uniform(0, 360),
            "pressure": np.random.uniform(950, 980),
            "precipitation": np.random.uniform(50, 100),
        }
    elif city in supported_cities:
        # Fetch live weather data from OpenWeatherMap
        live_weather = fetch_live_weather(city)
        if live_weather:
            return live_weather
    # Fallback to simulated data for unsupported cities
    return {
        "temperature": np.random.uniform(20, 40),
        "wind_speed": np.random.uniform(5, 20),
        "wind_direction": np.random.uniform(0, 360),
        "pressure": np.random.uniform(980, 1050),
        "precipitation": np.random.uniform(0, 10),
    }

# A* Search Algorithm for Flight Path Optimization
def a_star_search(start, end, cyclone, wind_data, pressure_data, precipitation_data):
    def heuristic(city):
        return geodesic(locations[city], locations[end]).km  # Distance to goal

    open_list = [(0, start, [])]  # Priority queue (cost, city, path)
    g_costs = {start: 0}  # Store shortest cost to reach each city

    while open_list:
        cost, city, path = heapq.heappop(open_list)
        path = path + [city]

        if city == end:
            st.write(f"✅ Rerouted flight path found: {path}")
            return path  # Return path when goal is reached

        for neighbor, (lat, lon) in locations.items():
            if neighbor != city and not is_affected(lat, lon, cyclone):  # Avoid cyclone-affected areas
                # Check if the **entire flight path** would enter the cyclone's radius
                if path_intersects_cyclone(locations[city], (lat, lon), cyclone):
                    continue  # Skip this city to avoid cyclone

                # Check weather conditions at the neighbor city
                wind_speed, wind_direction, pressure, precipitation = get_weather_at_location(lat, lon, wind_data, pressure_data, precipitation_data)

                # If wind speed is too high or pressure is too low, avoid the area
                if wind_speed > 80 or pressure < 950:
                    continue

                # Compute new cost
                new_cost = g_costs[city] + geodesic(locations[city], (lat, lon)).km
                if neighbor not in g_costs or new_cost < g_costs[neighbor]:
                    g_costs[neighbor] = new_cost
                    heapq.heappush(open_list, (new_cost + heuristic(neighbor), neighbor, path))

    st.write(f"❌ Flight from {start} to {end} CANCELED due to bad weather.")
    return None  # No valid path found

def path_intersects_cyclone(start_coords, end_coords, cyclone):
    """
    Checks if any part of the flight path between start and end passes through the cyclone's radius.
    Uses a step-wise check along the path.
    """
    num_steps = 100  # Increase this for better precision
    lat_step = (end_coords[0] - start_coords[0]) / num_steps
    lon_step = (end_coords[1] - start_coords[1]) / num_steps

    for i in range(num_steps + 1):
        lat = start_coords[0] + (i * lat_step)
        lon = start_coords[1] + (i * lon_step)

        if is_affected(lat, lon, cyclone):  # If any step is inside the cyclone
            return True  # The path intersects the cyclone

    return False  # Safe path

# Function to get weather at a specific location
def get_weather_at_location(lat, lon, wind_data, pressure_data, precipitation_data):
    for wind in wind_data:
        if wind[0] == lat and wind[1] == lon:
            wind_speed = wind[2]
            wind_direction = wind[3]
            break
    for pressure in pressure_data:
        if pressure[0] == lat and pressure[1] == lon:
            pressure_value = pressure[2]
            break
    for precipitation in precipitation_data:
        if precipitation[0] == lat and precipitation[1] == lon:
            precipitation_value = precipitation[2]
            break
    return wind_speed, wind_direction, pressure_value, precipitation_value

# Streamlit App
def main():
    st.title("Aviation Weather & Flight Path Optimization")

    # Cyclone Toggle Button
    if "cyclone_active" not in st.session_state:
        st.session_state.cyclone_active = False

    if st.button("Toggle Cyclone"):
        st.session_state.cyclone_active = not st.session_state.cyclone_active

    cyclone = simulate_cyclone() if st.session_state.cyclone_active else None

    # Weather prediction input
    st.subheader("Weather Prediction")
    selected_date = st.date_input("Select Date", datetime.today())
    selected_time = st.time_input("Select Time", datetime.now().time())

    # Map Initialization
    map_type = st.selectbox("Select Map Type", ["Temperature", "Wind", "Pressure", "Precipitation"])
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="cartodbdark_matter")

    # Generate weather data based on cyclone status
    temp_data = generate_temperature_data()
    wind_data = generate_wind_data(st.session_state.cyclone_active, cyclone)
    pressure_data = generate_pressure_data(st.session_state.cyclone_active, cyclone)
    precipitation_data = generate_precipitation_data(st.session_state.cyclone_active, cyclone)

    # Add cyclone to the map if active
    if cyclone:
        folium.Circle(
            location=[cyclone["lat"], cyclone["lon"]],
            radius=cyclone["radius"] * 111320,
            color="red",
            fill=True,
            fill_color="red"
        ).add_to(m)

    # Display Heatmaps
    if map_type == "Temperature":
        HeatMap(temp_data, min_opacity=0.3, max_opacity=0.5, radius=30).add_to(m)
    elif map_type == "Pressure":
        normalized_pressure = [
            [float(lat), float(lon), float((pressure - 950) / 100)]
            for lat, lon, pressure in pressure_data
            ]
        HeatMap(
            data=normalized_pressure,
            min_opacity=0.3,
            max_opacity=0.7,
            radius=35,
            gradient={"0.4": "lavender", "0.6": "mediumpurple", "0.8": "darkorchid", "1.0": "indigo"}  # Purple theme
        ).add_to(m)
        st.write("Pressure Scale: 950 hPa (dark purple) to 1050 hPa (light purple)")
    elif map_type == "Precipitation":
        normalized_precipitation = [
            [float(lat), float(lon), float(precipitation / 100)]
            for lat, lon, precipitation in precipitation_data
            ]
        HeatMap(
            data=normalized_precipitation,
            min_opacity=0.3,
            max_opacity=0.7,
            radius=35,
            gradient={"0.0": "white", "0.5": "lightblue", "1.0": "darkblue"}  # Blue theme
        ).add_to(m)
        st.write("Precipitation Scale: 0 mm (white) to 100 mm (dark blue)")
    elif map_type == "Wind":
        for lat, lon, wind_speed, wind_direction in wind_data:
            for _ in range(5):  # More arrows for better visualization
                rad = np.deg2rad(wind_direction)
                end_lat = lat + 0.2 * np.cos(rad)  # Larger arrow
                end_lon = lon + 0.2 * np.sin(rad)
                folium.PolyLine([(lat, lon), (end_lat, end_lon)], color="blue", weight=2 + wind_speed / 5, opacity=0.7).add_to(m)

    # Add city weather popups
    for city, (lat, lon) in cities.items():
        prediction = predict_weather(city, selected_date, selected_time, st.session_state.cyclone_active, cyclone)
        if prediction:
            popup_content = f"""
                <b>{city}</b><br>
                Temperature: {prediction['temperature']:.2f}°C<br>
                Wind Speed: {prediction['wind_speed']:.2f} km/h<br>
                Wind Direction: {prediction['wind_direction']:.2f}°<br>
                Pressure: {prediction['pressure']:.2f} hPa<br>
                Precipitation: {prediction['precipitation']:.2f} mm
            """
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color="blue")
            ).add_to(m)

    # Always display flight paths
    for name, (start, end) in flight_paths.items():
        start_lat, start_lon = locations[start]
        end_lat, end_lon = locations[end]

        # Original Flight Path
        folium.PolyLine([(start_lat, start_lon), (end_lat, end_lon)], color="darkblue", weight=3, opacity=0.8, popup=f"Original Path: {name}").add_to(m)

        # Rerouted Path (if cyclone is active)
        if cyclone:
            path = a_star_search(start, end, cyclone, wind_data, pressure_data, precipitation_data)
            if path:
                path_coords = [locations[city] for city in path]
                folium.PolyLine(path_coords, color="green", weight=3, opacity=1, popup=f"Rerouted Path: {name}").add_to(m)
                st.write(f"Flight '{name}' rerouted to avoid cyclone.")

    folium_static(m)

if __name__ == "__main__":
    main()