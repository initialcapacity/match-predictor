from unittest import TestCase

from matchpredictor.matchresults.result import Outcome
from matchpredictor.model.model_provider import ModelProvider, Model
from matchpredictor.predictors.predictor import Prediction


class TestModelProvider(TestCase):
    home_model = Model(name="home model", predictor=lambda _: Prediction(outcome=Outcome.HOME))
    away_model = Model(name="away model", predictor=lambda _: Prediction(outcome=Outcome.AWAY))

    provider = ModelProvider([home_model, away_model])

    def test_get_model(self) -> None:
        self.assertEqual(self.provider.get("home model"), self.home_model)
        self.assertEqual(self.provider.get("away model"), self.away_model)
        self.assertIsNone(self.provider.get("not there model"))

    def test_list(self) -> None:
        self.assertEqual(self.provider.list(), [self.home_model, self.away_model])
