from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np

data = pd.read_csv("outputs/fppg_py.csv")

gp_series = {}
for index, row in data.iterrows():
    player_name = row["full_name"]
    gp_data = row[12:23].replace(0, pd.NA).dropna()
    gp_data = pd.to_numeric(gp_data, errors="coerce").dropna()
    gp_data.index = np.arange(0, len(gp_data))
    gp_series[player_name] = gp_data


def predict(series):
    model = ARIMA(series, order=(1, 1, 1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=1)
    return forecast


predictions = {}
for player, series in gp_series.items():
    if len(series) > 0:
        try:
            prediction = predict(series)
            predictions[player] = prediction.iloc[0].round(0)
        except Exception as e:
            print(f"Error {e} with {player}")
    else:
        predictions[player] = np.nan

predictions_gp_df = pd.DataFrame(
    list(predictions.items()), columns=["Player", "Predicted_GP"]
)

for player, prediction in predictions.items():
    predictions_gp_df.to_csv("outputs/model2_gp_predictions.csv", index=False)
