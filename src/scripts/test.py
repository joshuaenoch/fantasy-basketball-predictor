import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

players = players.get_active_players()

spec_player = [player for player in players if player["full_name"] == "Jeremy Sochan"][
    0
]["id"]


career = playercareerstats.PlayerCareerStats(player_id=spec_player).get_data_frames()[0]
player_stats_2025 = career[career["SEASON_ID"] == "2024-25"]

print(player_stats_2025)
