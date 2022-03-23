from unittest import TestCase

from matchpredictor.matchresults.results_provider import validation_results
from matchpredictor.evaluation.evaluator import Evaluator
from matchpredictor.predictors.home_predictor import home_predictor


class TestHomePredictor(TestCase):
    def test_accuracy(self) -> None:
        validation_data = validation_results('spi_matches', 2019)
        accuracy, _ = Evaluator(home_predictor).measure_accuracy(validation_data)

        self.assertGreaterEqual(accuracy, .33)
