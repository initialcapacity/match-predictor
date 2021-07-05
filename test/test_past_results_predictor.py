from unittest import TestCase

from matchpredictor.matchresults.results_provider import load_results
from matchpredictor.predictors.past_results_predictor import PastResultsPredictor, calculate_table
from matchpredictor.evaluation.evaluator import Evaluator


class TestPastResultsPredictor(TestCase):
    def test_accuracy(self):
        results = load_results(data_file='england-training.csv')
        predictor = PastResultsPredictor(calculate_table(results))
        accuracy = Evaluator(predictor).measure_accuracy('england-validation.csv')

        self.assertGreaterEqual(accuracy, .33)

    def test_accuracy_last_two_seasons(self):
        results = load_results(
            data_file='england-training.csv',
            result_filter=lambda result: result.fixture.season >= 2017
        )
        predictor = PastResultsPredictor(calculate_table(results))
        accuracy = Evaluator(predictor).measure_accuracy('england-validation.csv')

        self.assertGreaterEqual(accuracy, .33)
