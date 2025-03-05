import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, VotingRegressor
import numpy as np

# Data loading
points_data = pd.read_csv("outputs/fppg_py.csv")

data_year1 = pd.read_csv("computed_data/new-2014-2015.csv")
data_year2 = pd.read_csv("computed_data/new-2015-2016.csv")
data_year3 = pd.read_csv("computed_data/new-2016-2017.csv")
data_year4 = pd.read_csv("computed_data/new-2017-2018.csv")
data_year5 = pd.read_csv("computed_data/new-2018-2019.csv")
data_year6 = pd.read_csv("computed_data/new-2019-2020.csv")
data_year7 = pd.read_csv("computed_data/new-2020-2021.csv")
data_year8 = pd.read_csv("computed_data/new-2021-2022.csv")
data_year9 = pd.read_csv("computed_data/new-2022-2023.csv")
data_year10 = pd.read_csv("computed_data/new-2023-2024.csv")
predicting_data = pd.read_csv("computed_data/new-2024-2025.csv")

data = [
    data_year1,
    data_year2,
    data_year3,
    data_year4,
    data_year5,
    data_year6,
    data_year7,
    data_year8,
    data_year9,
    data_year10,
]

# Fitting/transforming
num_atts = [
    "GP",
    "MIN",
    "FGM",
    "FGA",
    "FG3M",
    "FG3A",
    "FTM",
    "FTA",
    "OREB",
    "DREB",
    "REB",
    "AST",
    "STL",
    "BLK",
    "TOV",
    "PTS",
]
cat_atts = ["TEAM_ABBREVIATION"]
numeric_transformer = SimpleImputer(strategy="constant", fill_value=0)
preprocessor = ColumnTransformer(transformers=[("num", numeric_transformer, num_atts)])
models = []

# Model building
for year in range(len(data)):
    for col in num_atts:
        if col != "GP":
            data[year][col] = data[year][col] * data[year]["GP"]

    X = data[year][num_atts + cat_atts]
    y = data[year]["FPPG"] * data[year]["GP"]

    X = preprocessor.fit_transform(X)
    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

    model = RandomForestRegressor(random_state=1, n_estimators=300)
    model.fit(train_X, train_y)

    models.append((f"model_{year+1}", model))

print("finished models building")

# Predicting
voting_regressor = VotingRegressor(estimators=models)

combined_train_X = []
combined_train_y = []

for year in range(len(data)):
    X = data[year][num_atts + cat_atts]
    y = data[year]["FPPG"] * data[year]["GP"]
    X = preprocessor.transform(X)
    combined_train_X.append(X)
    combined_train_y.append(y)

combined_train_X = np.vstack(combined_train_X)
combined_train_y = np.concatenate(combined_train_y)

voting_regressor.fit(combined_train_X, combined_train_y)

# Predicting
for col in num_atts:
    if col != "GP":
        predicting_data[col] = predicting_data[col] * predicting_data["GP"]

X_test = predicting_data[num_atts + cat_atts]
X_test = preprocessor.transform(X_test)
predicted_fppg = voting_regressor.predict(X_test)
predicting_data["Predicted_FPPG"] = predicted_fppg

# Save predictions
predicting_data[["Player", "Predicted_FPPG"]].to_csv(
    "outputs/model1_all_predictions.csv", index=False
)

# Testing

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
)

actual_fppg = predicting_data["FPPG"].dropna().values
predicted_fppg = predicting_data["Predicted_FPPG"].dropna().values

if len(actual_fppg) == len(predicted_fppg):
    mae = mean_absolute_error(actual_fppg, predicted_fppg)
    mse = mean_squared_error(actual_fppg, predicted_fppg)
    rmse = np.sqrt(mse)
    mape = mean_absolute_percentage_error(actual_fppg, predicted_fppg)

    print(f"Mean Absolute Error: {mae}")
    print(f"Mean Squared Error: {mse}")
    print(f"Root Mean Squared Error: {rmse}")
    print(f"Mean Absolute Percentage Error: {mape}")
