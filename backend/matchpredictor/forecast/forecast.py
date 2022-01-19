from flask import Blueprint, jsonify, request, Response

from matchpredictor.forecast.forecaster import Forecaster


def forecast_api(forecaster: Forecaster) -> Blueprint:
    api = Blueprint("forecast_api", __name__)

    @api.route("/forecast", methods=["GET"])
    def forecast() -> Response:
        home_team = request.args['home_team']
        away_team = request.args['away_team']

        return jsonify(forecaster.forecast(
            home_team_name=home_team,
            away_team_name=away_team,
        ))

    return api
