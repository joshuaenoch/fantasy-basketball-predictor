from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd

testing_with = [
    "Jaylen Brown",
    "Jalen Williams",
    "Jalen Johnson",
    "Jalen Brunson",
    "Jaylin Williams",
    "Jalen Suggs",
    "Jalen Green",
]

players = players.get_active_players()
selected_players = [player for player in players if player["full_name"] in testing_with]

all_stats = []
for player in selected_players:
    career = playercareerstats.PlayerCareerStats(
        player_id=player["id"]
    ).get_data_frames()[0]
    player_stats_2025 = career[career["SEASON_ID"] == "2024-25"].iloc[0]

    all_stats.append(player_stats_2025.values)

stats_df = pd.DataFrame(
    all_stats,
    columns=[
        "PLAYER_ID",
        "SEASON_ID",
        "LEAGUE_ID",
        "TEAM_ID",
        "TEAM_ABBREVIATION",
        "PLAYER_AGE",
        "GP",
        "GS",
        "MIN",
        "FGM",
        "FGA",
        "FG_PCT",
        "FG3M",
        "FG3A",
        "FG3_PCT",
        "FTM",
        "FTA",
        "FT_PCT",
        "OREB",
        "DREB",
        "REB",
        "AST",
        "STL",
        "BLK",
        "TOV",
        "PF",
        "PTS",
    ],
)

stats_df["Player_Name"] = [player["full_name"] for player in selected_players]

stats_df = stats_df[
    ["Player_Name"] + [col for col in stats_df.columns if col != "Player_Name"]
]

per_game = [
    "MIN",
    "FGM",
    "FGA",
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

for i in per_game:
    stats_df[i] = stats_df[i] / stats_df["GP"]

stats_df.to_csv("stats.csv", index=False)
