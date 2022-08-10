from dataclasses import dataclass
from typing import List

from flask import Flask

from matchpredictor.forecast.forecast_api import forecast_api
from matchpredictor.forecast.forecaster import Forecaster
from matchpredictor.health import health_api
from matchpredictor.matchresults.result import Result
from matchpredictor.matchresults.results_provider import training_results
from matchpredictor.model.model_provider import ModelProvider, Model
from matchpredictor.model.models_api import models_api
from matchpredictor.predictors.home_predictor import HomePredictor
from matchpredictor.predictors.linear_regression_predictor import train_regression_predictor
from matchpredictor.predictors.past_results_predictor import train_results_predictor
from matchpredictor.predictors.simulation_predictor import train_offense_and_defense_predictor, train_offense_predictor
from matchpredictor.teams.teams_api import teams_api
from matchpredictor.teams.teams_provider import TeamsProvider
from matchpredictor.upcominggames.football_data_api_client import FootballDataApiClient
from matchpredictor.upcominggames.upcoming_games_api import upcoming_games_api


def build_model_provider(training_data: List[Result]) -> ModelProvider:
    return ModelProvider([
        Model("Home", HomePredictor()),
        Model("Points", train_results_predictor(training_data)),
        Model("Offense simulator (fast)", train_offense_predictor(training_data, 1_000)),
        Model("Offense simulator", train_offense_predictor(training_data, 10_000)),
        Model("Full simulator (fast)", train_offense_and_defense_predictor(training_data, 1_000)),
        Model("Full simulator", train_offense_and_defense_predictor(training_data, 10_000)),
        # The linear regression model uses scikit learn, so can cause issues on some machines
        # Model("Linear regression", train_regression_predictor(training_data))
    ])


@dataclass
class AppEnvironment:
    csv_location: str
    season: int
    football_data_api_key: str


def create_app(env: AppEnvironment) -> Flask:
    app = Flask(__name__)

    def last_two_years(result: Result) -> bool:
        return result.season >= env.season - 2

    results = training_results(env.csv_location, env.season, last_two_years)
    fixtures = list(map(lambda r: r.fixture, results))

    teams_provider = TeamsProvider(fixtures)
    models_provider = build_model_provider(results)
    forecaster = Forecaster(models_provider)
    football_data_api_client = FootballDataApiClient(env.football_data_api_key)

    app.register_blueprint(forecast_api(forecaster))
    app.register_blueprint(teams_api(teams_provider))
    app.register_blueprint(models_api(models_provider))
    app.register_blueprint(upcoming_games_api(football_data_api_client))
    app.register_blueprint(health_api())

    return app
