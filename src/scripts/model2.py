from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np

# Load the data
data = pd.read_csv("outputs/fppg_py.csv")

# Dictionary to store player series
players_series = {}

# Process each row in the data
for index, row in data.iterrows():
    player_name = row["full_name"]
    player_data = row[1:].replace(0, pd.NA).dropna()

    # Ensure the data is numeric and convert to pandas Series
    player_data = pd.to_numeric(player_data, errors="coerce").dropna()

    # Add a simple integer index if no datetime index is available
    player_data.index = range(len(player_data))

    players_series[player_name] = player_data


# Function to fit ARIMA model and predict
def predict_with_arima(series, order=(1, 1, 1)):
    model = ARIMA(series, order=order)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=1)
    return forecast.iloc[0]  # Use .iloc[0] to access the first forecasted value


# Predict for each player
predictions = {}
for player, series in players_series.items():
    if len(series) > 0:  # Ensure there is enough data to fit the model
        try:
            prediction = predict_with_arima(series)
            predictions[player] = prediction
        except Exception as e:
            print(f"Error predicting for {player}: {e}")

# Display predictions
for player, prediction in predictions.items():
    print(f"{player}: Predicted 2024-2025 result = {prediction:.2f}")
