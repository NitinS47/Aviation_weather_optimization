import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

def train_weather_model(input_file, output_file):
    data = pd.read_csv(input_file)
    # Features: Temperature, Humidity, Wind Speed
    X = data[['temperature', 'humidity', 'wind_speed']]
    # Target: Weather condition
    y = data['weather_condition']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    joblib.dump(model, output_file)
    print(f"Weather model saved to {output_file}")

if __name__ == "__main__":
    train_weather_model('data/processed/weather_data.csv', 'data/models/weather_model.pkl')
