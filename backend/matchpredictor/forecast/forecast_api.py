from flask import Blueprint, jsonify, request, Response

from matchpredictor.forecast.forecaster import Forecaster
from matchpredictor.matchresults.result import Team


def forecast_api(forecaster: Forecaster) -> Blueprint:
    api = Blueprint("forecast_api", __name__)

    @api.route("/forecast", methods=["GET"])
    def forecast() -> Response:
        home_name = request.args['home_name']
        home_country = request.args['home_country']
        away_name = request.args['away_name']
        away_country = request.args['away_country']

        return jsonify(forecaster.forecast(
            home_team=Team(name=home_name, country=home_country),
            away_team=Team(name=away_name, country=away_country),
        ))

    return api
