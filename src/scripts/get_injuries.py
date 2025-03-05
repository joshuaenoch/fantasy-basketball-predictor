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

injured_players = []
for player in all_players:
    if player.injured:
        injured_players.append(player.name)

with open("outputs/injuries.json", "w") as f:
    json.dump(injured_players, f)
