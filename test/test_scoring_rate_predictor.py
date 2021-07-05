from unittest import TestCase

from matchpredictor.predictors.scoring_rate_predictor import ScoringRatePredictor, calculate_scoring_rates
from matchpredictor.matchresults.results_provider import load_results
from matchpredictor.evaluation.evaluator import Evaluator


class TestScoringRatePredictor(TestCase):
    def test_accuracy_last_two_seasons(self):
        training_data = load_results('england-training.csv', result_filter=lambda result: result.fixture.season >= 2017)
        validation_data = load_results('england-validation.csv')
        predictor = ScoringRatePredictor(calculate_scoring_rates(training_data))

        accuracy = Evaluator(predictor).measure_accuracy(validation_data)

        self.assertGreaterEqual(accuracy, .33)
