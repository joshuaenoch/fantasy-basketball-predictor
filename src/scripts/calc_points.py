from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd
from datetime import datetime, timedelta

player_stats = pd.read_csv("stats.csv")

stats_weight = {
    "points": 1,
    "blocks": 4,
    "steals": 4,
    "assists": 2,
    "rebounds": 1,
    "turnovers": -2,
    "fgm": 2,
    "fga": -1,
    "ftm": 1,
    "fta": -1,
    "tpm": 1,
}

all_points = []
for index, row in player_stats.iterrows():
    points = (
        row["FGM"] * stats_weight["fgm"]
        + row["FGA"] * stats_weight["fga"]
        + row["FG3M"] * stats_weight["tpm"]
        + row["FTM"] * stats_weight["ftm"]
        + row["FTA"] * stats_weight["fta"]
        + row["REB"] * stats_weight["rebounds"]
        + row["AST"] * stats_weight["assists"]
        + row["STL"] * stats_weight["steals"]
        + row["BLK"] * stats_weight["blocks"]
        + row["TOV"] * stats_weight["turnovers"]
        + row["PTS"] * stats_weight["points"]
    )
    player = []
    player.append(row["Player_Name"])
    player.append(points)
    all_points.append(player)

all_points = pd.DataFrame(all_points, columns=["Player_Name", "Points"])
all_points.to_csv("points.csv", index=False)
