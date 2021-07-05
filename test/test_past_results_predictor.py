from unittest import TestCase

from matchpredictor.results.results_provider import load_results
from matchpredictor.predictors.past_results_predictor import PastResultsPredictor, calculate_table
from test.evaluator import measure_accuracy


class TestPastResultsPredictor(TestCase):
    def test_accuracy(self):
        results = load_results(file='england-training.csv')
        predictor = PastResultsPredictor(calculate_table(results))
        accuracy = measure_accuracy(predictor)

        self.assertGreaterEqual(accuracy, .33)

    def test_accuracy_last_two_seasons(self):
        results = load_results(
            file='england-training.csv',
            result_filter=lambda result: result.fixture.season >= 2017
        )
        predictor = PastResultsPredictor(calculate_table(results))
        accuracy = measure_accuracy(predictor)

        self.assertGreaterEqual(accuracy, .33)
