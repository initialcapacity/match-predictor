from flask import Blueprint, jsonify, Response

from matchpredictor.teams.teams_provider import TeamsProvider


def teams_api(teams_provider: TeamsProvider) -> Blueprint:
    api = Blueprint("teams_api", __name__)

    @api.route("/teams", methods=["GET"])
    def teams() -> Response:
        team_names = list(map(lambda team: team.name, teams_provider.unique_teams()))

        return jsonify({
            "teams": team_names
        })

    return api
