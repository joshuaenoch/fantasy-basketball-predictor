import pandas as pd

data = pd.read_csv("computed_data/chainging.csv")

keep_columns = [
    "Player",
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

metadata_columns = [
    "Player",
    "TEAM_ABBREVIATION",
]

tsv_data = data[keep_columns]
metadata = data[metadata_columns]

tsv_data.to_csv("computed_data/chaingingaling.csv", index=False)

metadata.to_csv("computed_data/chaingingaling_metadata.csv", index=False)
