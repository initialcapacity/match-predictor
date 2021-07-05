from unittest import TestCase

from matchpredictor.results.results_provider import load_results
from matchpredictor.predictors.past_results_predictor import PastResultsPredictor, calculate_table
from test.evaluator import measure_accuracy


class TestPastResultsPredictor(TestCase):
    def test_accuracy(self):
        predictor = self.__train_predictor()
        accuracy = measure_accuracy(predictor)

        self.assertGreaterEqual(accuracy, .33)

    def test_accuracy_last_two_seasons(self):
        predictor = self.__train_predictor(lambda result: result.fixture.season >= 2017)
        accuracy = measure_accuracy(predictor)

        self.assertGreaterEqual(accuracy, .33)

    @staticmethod
    def __train_predictor(result_filter=lambda result: True) -> PastResultsPredictor:
        results = list(filter(result_filter, load_results(file='england-training.csv')))
        return PastResultsPredictor(calculate_table(results))
