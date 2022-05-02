from unittest import TestCase

from matchpredictor.forecast.forecaster import Forecaster, Forecast
from matchpredictor.matchresults.result import Outcome, Team, Fixture
from matchpredictor.model.model_provider import ModelProvider, Model
from matchpredictor.predictors.predictor import Prediction, Predictor


class TestForecaster(TestCase):
    def setUp(self) -> None:
        super().setUp()

        home_model = Model(
            name="Home Model",
            predictor=type("Home", (Predictor, object), {"predict": lambda _, __: Prediction(outcome=Outcome.HOME)})()
        )
        away_model = Model(
            name="Away Model",
            predictor=type("Away", (Predictor, object), {"predict": lambda _, __: Prediction(outcome=Outcome.AWAY)})()
        )

        self.forecaster = Forecaster(ModelProvider([home_model, away_model]))

    def test_forecast_home(self) -> None:
        forecast = self.forecaster.forecast(
            Team(name='Chelsea'),
            Team(name='Burnley'),
            'UEFA Champions League',
            'Home Model',
        )

        self.assertEqual(forecast, Forecast(
            fixture=Fixture(
                home_team=Team(name='Chelsea'),
                away_team=Team(name='Burnley'),
                league='UEFA Champions League',
            ),
            model_name='Home Model',
            outcome=Outcome.HOME,
            confidence=None
        ))

    def test_forecast_away(self) -> None:
        forecast = self.forecaster.forecast(
            Team(name='Chelsea'),
            Team(name='Burnley'),
            'UEFA Champions League',
            'Away Model',
        )

        self.assertEqual(forecast, Forecast(
            fixture=Fixture(
                home_team=Team(name='Chelsea'),
                away_team=Team(name='Burnley'),
                league='UEFA Champions League',
            ),
            model_name='Away Model',
            outcome=Outcome.AWAY,
            confidence=None
        ))

    def test_forecast_model_none(self) -> None:
        forecast = self.forecaster.forecast(
            Team(name='Chelsea'),
            Team(name='Burnley'),
            'UEFA Champions League',
            'This model name does not exist'
        )

        self.assertIsNone(forecast)
