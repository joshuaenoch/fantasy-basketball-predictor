from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd
import time

batch_size = 20
delay_time = 15

players = players.get_active_players()
selected_players = players
stats = pd.DataFrame(
    columns=[
        "Player_Name",
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
    ]
)

redoing = []


def get_stats(selected_players):
    for i in range(0, len(selected_players), batch_size):
        batch_players = selected_players[i : i + batch_size]

        for player in batch_players:
            career = playercareerstats.PlayerCareerStats(
                player_id=player["id"]
            ).get_data_frames()[0]
            player_stats_2025 = career[career["SEASON_ID"] == "2024-25"]

            if not player_stats_2025.empty:
                player_stats_2025 = player_stats_2025.iloc[0]

                player_stats_2025["Player_Name"] = player["full_name"]

                if (player_stats_2025 == 0).sum() >= 3:
                    redoing.append(player)

                stats.loc[len(stats)] = player_stats_2025

        print(f"still going... {i+1}/{len(selected_players)}")
        time.sleep(delay_time)


get_stats(selected_players)

# before_length = 0
# count = 0
# while len(redoing) > 0 or count < 2:
#     before_length = len(redoing)
#     get_stats(redoing)
#     if before_length == len(redoing):
#         count += 1
#     redoing = []

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
    stats[col] = stats[col] / stats["GP"]

stats.to_csv("stats.csv", index=False)
