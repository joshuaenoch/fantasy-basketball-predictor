from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd
from nba_api.stats.endpoints import commonplayerinfo

data = pd.read_csv("outputs/gp_data.csv")
data2 = pd.read_csv("outputs/fppg_py.csv")

names = data2["full_name"].values
data["full_name"] = names

print(data)

data.to_csv("outputs/gp_data.csv", index=False)

# players = players.get_active_players()

# specific_player = [
#     player for player in players if player["full_name"] == "Dillon Brooks"
# ][0]

# career = playercareerstats.PlayerCareerStats(
#     player_id=specific_player["id"]
# ).get_data_frames()[0]
# print(career)
