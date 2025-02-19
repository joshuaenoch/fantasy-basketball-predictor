from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np

data = pd.read_csv("outputs/fppg_py.csv")

players_series = {}

# preprocess and time series creation
for index, row in data.iterrows():
    player_name = row["full_name"]
    player_data = row[1:].replace(0, pd.NA).dropna()

    player_data = pd.to_numeric(player_data, errors="coerce").dropna()

    player_data.index = range(len(player_data))

    players_series[player_name] = player_data


# model
def predict_with_arima(series, order=(1, 1, 1)):
    model = ARIMA(series, order=order)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=1)
    return forecast.iloc[0]


# get predictions for each player
predictions = {}
for player, series in players_series.items():
    if len(series) > 0:
        try:
            prediction = predict_with_arima(series)
            predictions[player] = prediction
        except Exception as e:
            print(f"Error with {player}")

for player, prediction in predictions.items():
    print(f"{player}: Predicted 2024-2025 result = {prediction:.2f}")

# testing
