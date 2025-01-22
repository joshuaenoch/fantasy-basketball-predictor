from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd
import time

players = players.get_active_players()
selected_players = players

all_stats = []
batch_size = 10
delay_time = 10

for i in range(0, len(selected_players), batch_size):
    batch_players = selected_players[i : i + batch_size]

    for player in batch_players:
        career = playercareerstats.PlayerCareerStats(
            player_id=player["id"]
        ).get_data_frames()[0]

        player_stats_2025 = career[career["SEASON_ID"] == "2024-25"]

        if not player_stats_2025.empty:
            player_stats_2025 = player_stats_2025.iloc[0]
            all_stats.append(player_stats_2025.values)

    print(f"still going... {i+1}/{len(selected_players)}")
    time.sleep(delay_time)

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

stats_df["Player_Name"] = [
    player["full_name"] for player in selected_players[: len(all_stats)]
]

stats_df = stats_df[
    ["Player_Name"] + [col for col in stats_df.columns if col != "Player_Name"]
]

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

for i in per_game:
    stats_df[i] = stats_df[i] / stats_df["GP"]

stats_df.to_csv("stats.csv", index=False)
