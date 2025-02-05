import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# data

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
]

# fitting/transforming

num_atts = [
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

# model building

for year in range(len(data)):
    X = data[year][num_atts + cat_atts]
    y = data[year]["FPPG"]

    X = preprocessor.fit_transform(X)
    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

    model = RandomForestRegressor(random_state=1)
    model.fit(train_X, train_y)

    models.append(model)

print("finished models building")

# model training

predicted_fppgs = []

for year in range(len(models)):
    X_test = predicting_data[num_atts + cat_atts]
    X_test = preprocessor.transform(X_test)
    predicted_fppg = models[year].predict(X_test)

    predicted_fppgs.append(predicted_fppg)

predicted_fppgs = np.array(predicted_fppgs)
average_predicted_fppg = predicted_fppgs.mean(axis=0)

predicting_data["Predicted_FPPG"] = average_predicted_fppg
predicting_data[["Player", "Predicted_FPPG"]].to_csv(
    "outputs/model1_predictions.csv", index=False
)

# testing

# from sklearn.metrics import mean_absolute_error

# predicting_data = pd.merge(
#     predicting_data,
#     points_data[["full_name", "2023-2024"]],
#     left_on="Player",
#     right_on="full_name",
#     how="left",
# )

# actual_fppg = predicting_data["FPPG"].dropna().values
# predicted_fppg = predicting_data["Predicted_FPPG"].dropna().values

# if len(actual_fppg) == len(predicted_fppg):
#     mae = mean_absolute_error(actual_fppg, predicted_fppg)
#     print(f"Mean Absolute Error (MAE): {mae}")
