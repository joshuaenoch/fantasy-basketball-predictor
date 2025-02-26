import pandas as pd
import numpy as np
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo

data = pd.read_csv("outputs/fppg_py.csv")
data_current = pd.read_csv("computed_data/new-2024-2025.csv")

ages = []
for index, row in data.iterrows():
    player = row["full_name"]
    if player in data_current["Player"].values:
        age = data_current.loc[data_current["Player"] == player]["PLAYER_AGE"].values[0]
        ages.append(age)
    else:
        ages.append(np.nan)

draft_years = []
for index, row in data.iterrows():
    player = row["full_name"]
    if player in data_current["Player"].values:
        player_id = data_current.loc[data_current["Player"] == player][
            "PLAYER_ID"
        ].values[0]
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_dict()
        draft_year = player_info["resultSets"][0]["rowSet"][0][29]
        draft_years.append(draft_year)
    else:
        draft_years.append(np.nan)

full_data = data.iloc[:, 12:23].copy()
full_data["Age"] = ages
full_data["Draft Year"] = draft_years

full_data.to_csv("outputs/gp_data.csv", index=False)
