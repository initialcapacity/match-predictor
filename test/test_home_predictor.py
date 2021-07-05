from unittest import TestCase

from matchpredictor.predictors.home_predictor import HomePredictor
from test.evaluator import measure_accuracy


class TestHomePredictor(TestCase):
    def test_accuracy(self):
        accuracy = measure_accuracy(HomePredictor())

        self.assertGreaterEqual(accuracy, .33)
