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

print(len(all_players))

print(all_players[0].injured)

exit()

agent_scores = []

for agent in free_agents:
    agent_score = {}
    stats = agent.stats
    agent_score["name"] = agent.name
    agent_score["score"] = stats["2025_last_7"]["applied_total"]
    agent_score["average"] = stats["2025_last_7"]["applied_avg"]
    agent_scores.append(agent_score)

agent_scores.sort(key=lambda x: x["score"], reverse=True)
agent_scores = agent_scores[:10]

print(agent_scores)
