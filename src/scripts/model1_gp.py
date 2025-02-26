import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    mean_absolute_percentage_error,
)

data = pd.read_csv("outputs/gp_data.csv").dropna()

y = data["gp_2024-2025"]
X = data.drop(["full_name", "gp_2024-2025"], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

model = RandomForestRegressor(random_state=1, n_estimators=300)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(y_pred)

print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("ROot Mean Squared Error:", root_mean_squared_error(y_test, y_pred))
print("Mean Absolute Percentage Error:", mean_absolute_percentage_error(y_test, y_pred))
