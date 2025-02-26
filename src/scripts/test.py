from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd
from nba_api.stats.endpoints import commonplayerinfo


# players = players.get_active_players()

# specific_player = [
#     player for player in players if player["full_name"] == "Dillon Brooks"
# ][0]

# career = playercareerstats.PlayerCareerStats(
#     player_id=specific_player["id"]
# ).get_data_frames()[0]
# print(career)
