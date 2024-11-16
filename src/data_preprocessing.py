import pandas as pd

def preprocess_weather_data(input_file, output_file):
    data = pd.read_csv(input_file)
    # Handle missing values
    data = data.fillna(method="ffill")
    # Convert timestamps to datetime
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    # Save processed data
    data.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

if __name__ == "__main__":
    preprocess_weather_data('data/raw/world_weather_data.csv', 'data/processed/weather_data.csv')
