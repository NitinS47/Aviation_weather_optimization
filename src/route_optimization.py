import networkx as nx
import pandas as pd
from geopy.distance import geodesic

def optimize_route(airports, routes, weather_data):
    G = nx.Graph()
    for _, row in routes.iterrows():
        source, dest = row['source'], row['destination']
        distance = geodesic(airports[source], airports[dest]).km
        weather_risk = weather_data.get((source, dest), 0)
        G.add_edge(source, dest, weight=distance + weather_risk)
    return nx.shortest_path(G, source='JFK', target='LAX', weight='weight')

if __name__ == "__main__":
    airports = {
        "JFK": (40.6413, -73.7781),
        "LAX": (33.9416, -118.4085),
        # Add more airports
    }
    routes = pd.read_csv('data/raw/flight_routes.csv')
    weather_data = {}  # Map of (source, destination) to risk value
    best_route = optimize_route(airports, routes, weather_data)
    print(f"Optimized route: {best_route}")
