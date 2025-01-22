from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd
from datetime import datetime, timedelta

player_stats = pd.read_csv("stats.csv")

months_convert = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12,
}
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
    print(f'{row["Player_Name"]}: {points}')
