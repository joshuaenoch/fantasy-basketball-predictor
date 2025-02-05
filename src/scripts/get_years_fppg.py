import pandas as pd
import numpy as np
from nba_api.stats.static import players

# all datasets
source_one = [
    "2014-2015",
    "2015-2016",
    "2016-2017",
    "2017-2018",
    "2018-2019",
    "2019-2020",
    "2020-2021",
    "2021-2022",
]
source_two = ["2022-2023", "2023-2024"]
source_three = ["2024-2025"]

# all active players
players = players.get_active_players()
all_points = pd.DataFrame(
    columns=["full_name"]
    + [year for year in source_one + source_two + source_three]
    + ["gp_" + year for year in source_one + source_two + source_three]
)
all_points["full_name"] = [player["full_name"] for player in players]

# stats weights for points calculation, will be customizeable by user
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


# gets the averages for datasets that have total stats
def get_averages(data):
    per_game = [
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
        "PF",
        "PTS",
    ]
    for col in per_game:
        data[col] = data[col] / data["GP"]
    return data


for dataset in source_one + source_two + source_three:

    # initial and end data
    df = pd.read_csv(f"season_data/{dataset}.csv")
    all_points[dataset] = np.zeros(len(all_points))
    all_points[f"gp_{dataset}"] = np.zeros(len(all_points))

    print("initialized", dataset)

    # make the data uniform
    if dataset in source_one:
        df = get_averages(df)
    elif dataset in source_two:
        df = (
            df.groupby("Player")
            .agg(
                {
                    "FGM": "mean",
                    "FGA": "mean",
                    "FG3M": "mean",
                    "FTM": "mean",
                    "FTA": "mean",
                    "REB": "mean",
                    "AST": "mean",
                    "STL": "mean",
                    "BLK": "mean",
                    "TOV": "mean",
                    "PTS": "mean",
                    "GP": "sum",
                }
            )
            .reset_index()
        )
    elif dataset in source_three:
        df = df.rename(columns={"Player_Name": "Player"})

    fppg = []
    for index, row in df.iterrows():
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
        fppg.append(points)

    # right here, add all the points as a new column "FPPG" to the current dataset
    df["FPPG"] = fppg

    df.to_csv(f"season_data/{dataset}.csv", index=False)
    print("finished", dataset)

# all_points.to_csv("fppg_py.csv", index=False)
