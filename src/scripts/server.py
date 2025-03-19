from flask import Flask, request, jsonify
from flask_cors import CORS
from espn_api.basketball import League
import json
import os

app = Flask(__name__)
CORS(app)


def run_python_function(league_id, team_id):
    league = League(league_id=league_id, year=2025)
    teams = league.teams

    my_team = "not found"

    for team in teams:
        if team.team_id == team_id:
            my_team = team

    team_data = {
        "team_name": my_team.team_name,
        "wins": my_team.wins,
        "losses": my_team.losses,
        "standing": my_team.standing,
        "roster": [],
        "free_agents": [],
        "top_agents": [],
    }

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

    # Save data to JSON file
    os.makedirs("outputs", exist_ok=True)
    team_json = json.dumps(team_data, indent=4)
    # with open("outputs/fantasy_data.json", "w") as json_file:
    #     json_file.write(team_json)

    return team_data


@app.route("/run-script", methods=["POST"])
def run_script():
    data = request.get_json()
    league_id = int(data["leagueId"])
    team_id = int(data["teamId"])

    result = run_python_function(league_id, team_id)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
