from flask import Blueprint, jsonify, request, Response

from matchpredictor.forecast.forecaster import Forecaster
from matchpredictor.matchresults.result import Team


def forecast_api(forecaster: Forecaster) -> Blueprint:
    api = Blueprint("forecast_api", __name__)

    @api.route("/forecast", methods=["GET"])
    def forecast() -> Response:
        home_name = request.args['home_name']
        away_name = request.args['away_name']
        league = request.args['league']
        model_name = request.args['model_name']

        return jsonify(forecaster.forecast(
            home_team=Team(name=home_name),
            away_team=Team(name=away_name),
            league=league,
            model_name=model_name
        ))

    return api
