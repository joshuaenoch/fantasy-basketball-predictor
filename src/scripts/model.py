import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor

points = pd.read_csv("points.csv")
stats = pd.read_csv("stats.csv")

data = pd.merge(points, stats, on="Player_Name")

y = data["Points"]

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

X = data[["Player_Name"] + num_atts]

numeric_transformer = SimpleImputer(strategy="constant", fill_value=0)
preprocessor = ColumnTransformer(transformers=[("num", numeric_transformer, num_atts)])

X = preprocessor.fit_transform(X)

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

model = RandomForestRegressor(random_state=1)
model.fit(train_X, train_y)
test_predictions = model.predict(val_X)

print("MAE: ", mean_absolute_error(test_predictions, val_y))

predictions = model.predict(X)

points["Predicted_Points"] = predictions

points.to_csv("predictions.csv", index=False)
