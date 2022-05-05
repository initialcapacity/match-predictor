from unittest import TestCase

from matchpredictor.matchresults.result import Outcome, Fixture, Scenario
from matchpredictor.model.model_provider import ModelProvider, Model
from matchpredictor.predictors.predictor import Prediction, Predictor, InProgressPredictor


class Home(Predictor):
    def predict(self, fixture: Fixture) -> Prediction:
        return Prediction(outcome=Outcome.HOME)


class Away(InProgressPredictor):
    def predict(self, fixture: Fixture) -> Prediction:
        return Prediction(outcome=Outcome.AWAY)

    def predict_in_progress(self, fixture: Fixture, scenario: Scenario) -> Prediction:
        return Prediction(outcome=Outcome.DRAW)


class TestModelProvider(TestCase):
    home_predictor = Home()
    home_model = Model(
        name="home model",
        predictor=home_predictor
    )
    away_predictor = Away()
    away_model = Model(
        name="away model",
        predictor=away_predictor
    )

    provider = ModelProvider([home_model, away_model])

    def test_get_predictor(self) -> None:
        self.assertEqual(self.provider.get_predictor("home model"), self.home_predictor)
        self.assertEqual(self.provider.get_predictor("away model"), self.away_predictor)
        self.assertIsNone(self.provider.get_predictor("draw model"))
        self.assertIsNone(self.provider.get_predictor("not there model"))

    def test_get_in_progress_predictor(self) -> None:
        self.assertEqual(self.provider.get_in_progress_predictor("away model"), self.away_predictor)

        self.assertIsNone(self.provider.get_in_progress_predictor("home model"))
        self.assertIsNone(self.provider.get_in_progress_predictor("not there model"))

    def test_list(self) -> None:
        self.assertEqual(self.provider.list(), [self.home_model, self.away_model])
