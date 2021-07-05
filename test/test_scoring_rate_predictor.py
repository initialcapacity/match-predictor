from unittest import TestCase

from matchpredictor.predictors.scoring_rate_predictor import ScoringRatePredictor, calculate_scoring_rates
from matchpredictor.results.results_provider import load_results
from test.evaluator import measure_accuracy


class TestScoringRatePredictor(TestCase):
    def test_accuracy_last_two_seasons(self):
        results = load_results(file='england-training.csv', result_filter=lambda result: result.fixture.season >= 2018)
        predictor = ScoringRatePredictor(calculate_scoring_rates(results))
        accuracy = measure_accuracy(predictor)

        self.assertGreaterEqual(accuracy, .33)
