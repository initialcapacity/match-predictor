from unittest import TestCase

from matchpredictor.predictors.scoring_rate_predictor import ScoringRatePredictor, calculate_scoring_rates
from matchpredictor.results.results_provider import load_results
from matchpredictor.predictors.past_results_predictor import PastResultsPredictor, calculate_table
from test.evaluator import measure_accuracy


class TestScoringRatePredictor(TestCase):
    def test_accuracy_last_two_seasons(self):
        predictor = self.__train_predictor(lambda result: result.fixture.season >= 2018)
        accuracy = measure_accuracy(predictor)

        self.assertGreaterEqual(accuracy, .33)

    @staticmethod
    def __train_predictor(result_filter=lambda result: True) -> ScoringRatePredictor:
        results = list(filter(result_filter, load_results(file='england-training.csv')))
        return ScoringRatePredictor(calculate_scoring_rates(results))
