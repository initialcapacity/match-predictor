from unittest import TestCase

from matchpredictor.evaluation.evaluator import Evaluator
from matchpredictor.matchresults.results_provider import load_results
from matchpredictor.predictors.linear_regression_predictor import train_regression_predictor
from matchpredictor.predictors.scoring_rate_predictor import train_scoring_predictor


class TestLinearRegressionPredictor(TestCase):
    def test_accuracy(self):
        training_data = load_results('england-training.csv', result_filter=lambda result: result.fixture.season >= 2015)
        validation_data = load_results('england-validation.csv')
        predictor = train_regression_predictor(training_data)

        accuracy, _ = Evaluator(predictor).measure_accuracy(validation_data)

        self.assertGreaterEqual(accuracy, .33)
