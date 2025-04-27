import pickle
import pandas as pd
import numpy as np

# Load the .pkl file
with open("weather_model.pkl", "rb") as f:
    data = pickle.load(f)

# Check the type of the loaded object
print("Type of object in .pkl file:", type(data))

# If the object is a DataFrame (dataset)
if isinstance(data, pd.DataFrame):
    print("First row of the dataset:")
    print(data.iloc[0])  # Display the first row

# If the object is a NumPy array
elif isinstance(data, np.ndarray):
    print("First row of the array:")
    print(data[0])  # Display the first row

# If the object is a machine learning model
elif hasattr(data, "predict"):  # Check if it's a model
    print("This is a machine learning model.")
    if hasattr(data, "feature_names_in_"):  # Check if feature names are available
        print("Input features (headings):", data.feature_names_in_)
    else:
        print("Feature names are not available.")

# If the object is a dictionary
elif isinstance(data, dict):
    print("First key-value pair in the dictionary:")
    print(list(data.items())[0])  # Display the first key-value pair

# If the object is a list
elif isinstance(data, list):
    print("First element in the list:")
    print(data[0])  # Display the first element

# For other types of objects
else:
    print("Object type not recognized. Here's the object:")
    print(data)