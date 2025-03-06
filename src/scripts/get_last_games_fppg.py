from espn_api.basketball import League
import pandas as pd
import json


league = League(league_id=2073613821, year=2025)

all_players = []


teams = league.teams

my_team = "not found"

for team in teams:
    for player in team.roster:
        all_players.append(player)

free_agents = league.free_agents(size=None)

for player in free_agents:
    all_players.append(player)


players_last_stats = []
for player in all_players:
    player_stats = {
        "name": player.name,
        "7_fppg": player.stats["2025_last_7"]["applied_avg"],
        "30_fppg": player.stats["2025_last_30"]["applied_avg"],
    }
    players_last_stats.append(player_stats)

with open("outputs/last_stats.json", "w") as f:
    json.dump(players_last_stats, f)
