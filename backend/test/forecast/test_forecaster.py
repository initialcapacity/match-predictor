from unittest import TestCase
from matchpredictor.matchresults.result import Outcome, Team, Fixture
from matchpredictor.predictors.predictor import Prediction
from matchpredictor.forecast.forecaster import Forecaster, Forecast


class TestForecaster(TestCase):
    def test_forecast(self) -> None:
        def predictor(_: Fixture) -> Prediction:
            return Prediction(outcome=Outcome.HOME, confidence=.78)

        forecaster = Forecaster(predictor)

        forecast = forecaster.forecast(
            Team(name='Chelsea'),
            Team(name='Burnley'),
            'UEFA Champions League',
        )

        self.assertEqual(forecast, Forecast(
            fixture=Fixture(
                home_team=Team(name='Chelsea'),
                away_team=Team(name='Burnley'),
                league='UEFA Champions League',
            ),
            outcome=Outcome.HOME,
            confidence=.78
        ))
