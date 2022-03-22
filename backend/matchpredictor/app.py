from flask import Flask

from matchpredictor.forecast.forecast_api import forecast_api
from matchpredictor.forecast.forecaster import Forecaster
from matchpredictor.health import health_api
from matchpredictor.matchresults.result import Result
from matchpredictor.matchresults.results_provider import training_results
from matchpredictor.predictors.simulation_predictor import train_offense_and_defense_predictor
from matchpredictor.teams.teams_api import teams_api
from matchpredictor.teams.teams_provider import TeamsProvider

app = Flask(__name__)

season = 2022


def last_two_years(result: Result) -> bool:
    return result.season >= season - 2


results = training_results("spi_matches", season, last_two_years)
fixtures = list(map(lambda r: r.fixture, results))

teams_provider = TeamsProvider(fixtures)
predictor = train_offense_and_defense_predictor(results, 300)
forecaster = Forecaster(predictor)

app.register_blueprint(forecast_api(forecaster))
app.register_blueprint(teams_api(teams_provider))
app.register_blueprint(health_api())
