import logging
import json
from espn_api.basketball import League

league = League(league_id=187113096, year=2025)

teams = league.teams

my_team = "not found"

for team in teams:
    if team.team_id == 2:
        my_team = team

# Create a dictionary for the team data
team_data = {
    "team_name": my_team.team_name,
    "wins": my_team.wins,
    "losses": my_team.losses,
    "standing": my_team.standing,
    "roster": [],
    "free_agents": [],
    "top_agents": [],
}

# Populate the roster data
roster = my_team.roster

for player in roster:
    player_data = {
        "name": player.name,
        "position": player.position,
        "avg_points": player.avg_points,
        "avg_points_7": player.stats["2025_last_7"]["applied_avg"],
        "injured": player.injured,
    }
    team_data["roster"].append(player_data)

free_agents = league.free_agents()

free_agent_data = []
for player in free_agents:
    player_data = {
        "name": player.name,
        "position": player.position,
        "avg_points": player.avg_points,
        "injured": player.injured,
    }
    free_agent_data.append(player_data)

free_agent_data.sort(key=lambda x: x["avg_points"], reverse=True)

team_data["free_agents"] = free_agent_data

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

team_data["top_agents"] = agent_scores

team_json = json.dumps(team_data, indent=4)

with open("outputs/fantasy_data.json", "w") as json_file:
    json_file.write(team_json)
