from espn_api.basketball import League

league = League(league_id=2073613821, year=2025)


teams = league.teams

my_team = "not found"

for team in teams:
    if team.team_id == 4:
        my_team = team


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

print(free_agent_data)
