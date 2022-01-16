from flask import Blueprint, jsonify, request

from matchpredictor.forecast.forecaster import Forecaster


def forecast_api(season, forecaster: Forecaster):
    api = Blueprint("forecast_api", __name__)

    @api.route(f"/<string:league>/{season}", methods=["GET"])
    def forecast(league: str):
        home_team = request.args['home_team']
        away_team = request.args['away_team']

        outcome = forecaster.forecast(
            league=league,
            home_team_name=home_team,
            away_team_name=away_team,
            season=season,
        )

        return jsonify({"outcome": outcome})

    return api
