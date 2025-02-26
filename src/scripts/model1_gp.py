import pandas as pd

data = pd.to_csv("outputs/fppg_py.csv")
data_current = pd.to_csv("computed_data/new-2024-2025.csv")

ages = []
for index, row in data.iterrows():
    player = row["full_name"]
    if player in data_current["Player"].values:
        age = data_current.loc[data_current["Player"] == player]["AGE"].values[0]
        ages.append(age)

data["AGE"] = ages

print(data)
