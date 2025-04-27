from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fetch_weather import fetch_live_weather, simulate_cyclone
from dijkstra import dijkstra

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Streamlit
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/fetch-weather")
def get_weather(lat: float, lon: float):
    return fetch_live_weather(lat, lon)

@app.get("/simulate-cyclone")
def get_cyclone(lat: float = 20.5937, lon: float = 78.9629, radius: float = 500):
    return simulate_cyclone(lat, lon, radius)

@app.get("/optimize-flight-path")
def optimize_path(start: str, end: str):
    # Example graph (replace with real data)
    graph = {
        "Delhi": {"Mumbai": 10, "Bangalore": 20},
        "Mumbai": {"Delhi": 10, "Bangalore": 15},
        "Bangalore": {"Delhi": 20, "Mumbai": 15, "Dubai": 30},
        "Dubai": {"Bangalore": 30},
    }
    shortest_path_cost = dijkstra(graph, start, end)
    return {"shortest_path_cost": shortest_path_cost}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)