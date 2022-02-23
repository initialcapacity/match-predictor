from flask import Flask

from matchpredictor.forecast.forecast import forecast_api
from matchpredictor.forecast.forecaster import Forecaster
from matchpredictor.health import health_api
from matchpredictor.matchresults.result import Result
from matchpredictor.matchresults.results_provider import training_results
from matchpredictor.predictors.scoring_rate_predictor import train_scoring_predictor
from matchpredictor.teams.teams_api import teams_api
from matchpredictor.teams.teams_provider import TeamsProvider

app = Flask(__name__)

season = 2020


def last_two_years(result: Result) -> bool:
    return result.season >= season - 2


england_training_data = training_results('england.csv', season, last_two_years)
italy_training_data = training_results('italy.csv', season, last_two_years)
germany_training_data = training_results('germany.csv', season, last_two_years)

results = england_training_data + italy_training_data + germany_training_data
fixtures = list(map(lambda r: r.fixture, results))

teams_provider = TeamsProvider(fixtures)
predictor = train_scoring_predictor(results, 300)
forecaster = Forecaster(predictor)

app.register_blueprint(forecast_api(forecaster))
app.register_blueprint(teams_api(teams_provider))
app.register_blueprint(health_api())
