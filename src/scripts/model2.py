from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd
import numpy as np

# Load data
data = pd.read_csv("outputs/fppg_py.csv")

data_years = [
    pd.read_csv("computed_data/new-2014-2015.csv"),
    pd.read_csv("computed_data/new-2015-2016.csv"),
    pd.read_csv("computed_data/new-2016-2017.csv"),
    pd.read_csv("computed_data/new-2017-2018.csv"),
    pd.read_csv("computed_data/new-2018-2019.csv"),
    pd.read_csv("computed_data/new-2019-2020.csv"),
    pd.read_csv("computed_data/new-2020-2021.csv"),
    pd.read_csv("computed_data/new-2021-2022.csv"),
    pd.read_csv("computed_data/new-2022-2023.csv"),
    pd.read_csv("computed_data/new-2023-2024.csv"),
]
predicting_data = pd.read_csv("computed_data/new-2024-2025.csv")

players_series = {}
min_series = {}

# Preprocess the data and create time series for each player
for index, row in data.iterrows():
    player_name = row["full_name"]
    player_data = row[1:11].replace(0, pd.NA).dropna()
    player_data = pd.to_numeric(player_data, errors="coerce").dropna()
    player_data.index = np.arange(0, len(player_data))
    players_series[player_name] = player_data

for index, row in data.iterrows():
    player_name = row["full_name"]
    player_minutes = []
    for year_data in data_years:
        if player_name in year_data["Player"].values:
            minutes_value = year_data.loc[year_data["Player"] == player_name][
                "MIN"
            ].values[0]
            player_minutes.append(pd.to_numeric(minutes_value, errors="coerce"))
    min_series[player_name] = pd.Series(player_minutes).dropna().reset_index(drop=True)

print(players_series["Steven Adams"])
print(min_series["Steven Adams"])


# Model function
def predict(series, exog, order=(1, 1, 1), seasonal_order=(0, 0, 0, 0)):
    model = SARIMAX(series, exog=exog, order=order, seasonal_order=seasonal_order)
    model_fit = model.fit(disp=False)
    forecast = model_fit.forecast(steps=1, exog=exog[-1:])
    return forecast.iloc[0]


# Get predictions for each player
predictions = {}
for player, series in players_series.items():
    if len(series) > 0 and player in min_series:
        try:
            exog = min_series[player]
            exog = exog.reset_index(drop=True)
            prediction = predict(series, exog)
            predictions[player] = prediction
        except Exception as e:
            print(f"Error {e} with {player}")

predictions_df = pd.DataFrame(
    list(predictions.items()), columns=["Player", "Predicted_FPPG"]
)
for player, prediction in predictions.items():
    predictions_df.to_csv("outputs/model2_predictions.csv", index=False)

# Testing
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
)

actual_fppg = (
    data[data["full_name"].isin(predictions.keys())]["2024-2025"].dropna().values
)
predicted_fppg = np.array(list(predictions.values()))

if len(actual_fppg) == len(predicted_fppg):
    mae = mean_absolute_error(actual_fppg, predicted_fppg)
    mse = mean_squared_error(actual_fppg, predicted_fppg)
    rmse = np.sqrt(mse)
    mape = mean_absolute_percentage_error(actual_fppg, predicted_fppg)

    non_zero_actual_fppg = actual_fppg[actual_fppg != 0]
    non_zero_predicted_fppg = predicted_fppg[actual_fppg != 0]

    if len(non_zero_actual_fppg) > 0:
        mape = mean_absolute_percentage_error(
            non_zero_actual_fppg, non_zero_predicted_fppg
        )
    else:
        mape = np.nan

    print(f"Mean Absolute Error: {mae}")
    print(f"Mean Squared Error: {mse}")
    print(f"Root Mean Squared Error: {rmse}")
    print(f"Mean Absolute Percentage Error: {mape}")
else:
    print(len(actual_fppg), len(predicted_fppg))
