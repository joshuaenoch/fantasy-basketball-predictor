import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
)

data = pd.read_csv("outputs/gp_data.csv").dropna()

y = data["gp_2024-2025"]

gp_columns = [
    "gp_2015-2016",
    "gp_2016-2017",
    "gp_2017-2018",
    "gp_2018-2019",
    "gp_2019-2020",
    "gp_2020-2021",
    "gp_2021-2022",
    "gp_2022-2023",
    "gp_2023-2024",
]


def average_excluding_leading_zeros(row):
    non_zero_row = row[(row != 0) | (row.cummax() != 0)]
    return non_zero_row.mean()


avg_gp = data[gp_columns].apply(average_excluding_leading_zeros, axis=1)

X = pd.DataFrame()
X["Avg_GP"] = avg_gp
X["Age"] = data["Age"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

model = RandomForestRegressor(random_state=1, n_estimators=300)
model.fit(X_train, y_train)

y_pred_full = model.predict(X)
y_pred_full = np.round(y_pred_full)

data["Predicted_GP"] = y_pred_full

pred_gp = pd.DataFrame()
pred_gp["Player"] = data["full_name"]
pred_gp["Predicted_GP"] = y_pred_full

pred_gp.to_csv("outputs/model1_gp_predictions.csv", index=False)


y_pred_test = model.predict(X_test)
y_pred_test = np.round(y_pred_test)

print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred_test))
print("Mean Squared Error:", mean_squared_error(y_test, y_pred_test))
print("Root Mean Squared Error:", np.sqrt(mean_squared_error(y_test, y_pred_test)))
print(
    "Mean Absolute Percentage Error:",
    mean_absolute_percentage_error(y_test, y_pred_test),
)
