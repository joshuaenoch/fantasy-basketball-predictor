import logging
import json
from espn_api.basketball import League

league = League(league_id=2073613821, year=2025)

teams = league.teams

my_team = "not found"

for team in teams:
    if team.team_id == 4:
        my_team = team

# Create a dictionary for the team data
team_data = {
    "team_name": my_team.team_name,
    "wins": my_team.wins,
    "losses": my_team.losses,
    "standing": my_team.standing,
    "roster": [],
    "free_agents": [],
}

# Populate the roster data
roster = my_team.roster

for player in roster:
    player_data = {
        "name": player.name,
        "position": player.position,
        "avg_points": player.avg_points,
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

team_json = json.dumps(team_data, indent=4)

with open("outputs/fantasy_data.json", "w") as json_file:
    json_file.write(team_json)
