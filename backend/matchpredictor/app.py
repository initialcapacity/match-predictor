from flask import Flask

from matchpredictor.forecast.forecast import forecast_api
from matchpredictor.forecast.forecaster import Forecaster
from matchpredictor.health import health_api
from matchpredictor.matchresults.result import Result
from matchpredictor.matchresults.results_provider import training_results
from matchpredictor.predictors.linear_regression_predictor import train_regression_predictor
from matchpredictor.predictors.predictor import PredictorProvider

app = Flask(__name__)

season = 2020


def last_two_years(result: Result) -> bool:
    return result.season >= season - 2


england_training_data = training_results('england.csv', season, last_two_years)
italy_training_data = training_results('italy.csv', season, last_two_years)
france_training_data = training_results('france.csv', season, last_two_years)

provider = PredictorProvider()
provider.add("england", train_regression_predictor(england_training_data))
provider.add("italy", train_regression_predictor(italy_training_data))
provider.add("france", train_regression_predictor(france_training_data))
forecaster = Forecaster(provider)

app.register_blueprint(forecast_api(forecaster), url_prefix="/forecast")
app.register_blueprint(health_api())
