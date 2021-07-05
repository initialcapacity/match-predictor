from unittest import TestCase

from matchpredictor.predictors.home_predictor import HomePredictor
from matchpredictor.evaluation.evaluator import Evaluator


class TestHomePredictor(TestCase):
    def test_accuracy(self):
        accuracy = Evaluator(HomePredictor()).measure_accuracy('england-validation.csv')

        self.assertGreaterEqual(accuracy, .33)
