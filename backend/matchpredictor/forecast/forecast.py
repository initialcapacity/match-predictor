from typing import Optional

from flask import Blueprint, jsonify, request, Response

from matchpredictor.forecast.forecaster import Forecaster, Forecast


def forecast_api(season: int, forecaster: Forecaster) -> Blueprint:
    api = Blueprint("forecast_api", __name__)

    @api.route(f"/<string:league>/{season}", methods=["GET"])
    def forecast(league: str) -> Response:
        home_team = request.args['home_team']
        away_team = request.args['away_team']

        return jsonify(forecaster.forecast(
            league=league,
            home_team_name=home_team,
            away_team_name=away_team,
            season=season,
        ))

    return api
