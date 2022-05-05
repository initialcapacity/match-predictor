from unittest import TestCase

from matchpredictor.forecast.forecaster import Forecaster, Forecast
from matchpredictor.matchresults.result import Outcome, Team, Fixture, Scenario
from matchpredictor.model.model_provider import ModelProvider, Model
from matchpredictor.predictors.predictor import Prediction, Predictor, InProgressPredictor


class Home(Predictor):
    def predict(self, fixture: Fixture) -> Prediction:
        return Prediction(outcome=Outcome.HOME)


class Away(InProgressPredictor):
    def predict_in_progress(self, fixture: Fixture, scenario: Scenario) -> Prediction:
        return Prediction(outcome=Outcome.AWAY)

    def predict(self, fixture: Fixture) -> Prediction:
        return Prediction(outcome=Outcome.AWAY)


class TestForecaster(TestCase):
    home_model = Model(
        name="Home",
        predictor=Home()
    )
    away_model = Model(
        name="Away",
        predictor=Away()
    )

    forecaster = Forecaster(ModelProvider([home_model, away_model]))

    def test_forecast_home(self) -> None:
        forecast = self.forecaster.forecast(
            Fixture(
                Team(name='Chelsea'),
                Team(name='Burnley'),
                'UEFA Champions League',
            ),
            'Home',
        )

        self.assertEqual(forecast, Forecast(
            fixture=Fixture(
                home_team=Team(name='Chelsea'),
                away_team=Team(name='Burnley'),
                league='UEFA Champions League',
            ),
            model_name='Home',
            outcome=Outcome.HOME,
            confidence=None
        ))

    def test_forecast_away(self) -> None:
        forecast = self.forecaster.forecast(
            Fixture(
                Team(name='Chelsea'),
                Team(name='Burnley'),
                'UEFA Champions League',
            ),
            'Away',
        )

        self.assertEqual(forecast, Forecast(
            fixture=Fixture(
                home_team=Team(name='Chelsea'),
                away_team=Team(name='Burnley'),
                league='UEFA Champions League',
            ),
            model_name='Away',
            outcome=Outcome.AWAY,
            confidence=None
        ))

    def test_forecast_model_none(self) -> None:
        forecast = self.forecaster.forecast(
            Fixture(
                Team(name='Chelsea'),
                Team(name='Burnley'),
                'UEFA Champions League',
            ),
            'This model name does not exist'
        )

        self.assertIsNone(forecast)

    def test_forecast_in_progress_away(self) -> None:
        forecast = self.forecaster.forecast_in_progress(
            Fixture(
                Team(name='Chelsea'),
                Team(name='Burnley'),
                'UEFA Champions League',
            ),
            Scenario(30, 1, 2),
            'Away',
        )

        self.assertEqual(forecast, Forecast(
            fixture=Fixture(
                home_team=Team(name='Chelsea'),
                away_team=Team(name='Burnley'),
                league='UEFA Champions League',
            ),
            model_name='Away',
            outcome=Outcome.AWAY,
            confidence=None
        ))

    def test_forecast_in_progress_no_model(self) -> None:
        forecast = self.forecaster.forecast_in_progress(
            Fixture(
                Team(name='Chelsea'),
                Team(name='Burnley'),
                'UEFA Champions League',
            ),
            Scenario(30, 1, 2),
            'Home'
        )

        self.assertIsNone(forecast)
