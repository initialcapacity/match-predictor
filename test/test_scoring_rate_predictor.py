from unittest import TestCase

from matchpredictor.predictors.scoring_rate_predictor import ScoringRatePredictor, calculate_scoring_rates
from matchpredictor.matchresults.results_provider import load_results
from matchpredictor.evaluation.evaluator import Evaluator


class TestScoringRatePredictor(TestCase):
    def test_accuracy_last_two_seasons(self):
        results = load_results(data_file='england-training.csv', result_filter=lambda result: result.fixture.season >= 2018)
        predictor = ScoringRatePredictor(calculate_scoring_rates(results))
        accuracy = Evaluator(predictor).measure_accuracy('england-validation.csv')

        self.assertGreaterEqual(accuracy, .33)
