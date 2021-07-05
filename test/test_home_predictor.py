from unittest import TestCase

from matchpredictor.matchresults.results_provider import load_results
from matchpredictor.predictors.home_predictor import HomePredictor
from matchpredictor.evaluation.evaluator import Evaluator


class TestHomePredictor(TestCase):
    def test_accuracy(self):
        validation_data = load_results('england-validation.csv')
        accuracy = Evaluator(HomePredictor()).measure_accuracy(validation_data)

        self.assertGreaterEqual(accuracy, .33)
