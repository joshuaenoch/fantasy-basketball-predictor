import pandas as pd

df = pd.read_csv("computed_data/new-2024-2025.csv")

for index, row in df.iterrows():
    for col in df.columns:
        if isinstance(row[col], (int, float)):
            if "." in str(row[col]) and len(str(row[col]).split(".")[1]) > 2:
                df.at[index, col] = round(
                    row[col], 2
                )  # Update the DataFrame with the rounded value

df.to_csv("computed_data/new-2024-2025.csv", index=False)

# from nba_api.stats.static import players
# from nba_api.stats.endpoints import playercareerstats

# players = players.get_active_players()

# spec_player = [player for player in players if player["full_name"] == "Jeremy Sochan"][
#     0
# ]["id"]


# career = playercareerstats.PlayerCareerStats(player_id=spec_player).get_data_frames()[0]
# player_stats_2025 = career[career["SEASON_ID"] == "2024-25"]

# print(player_stats_2025)
