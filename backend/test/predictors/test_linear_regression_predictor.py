from unittest import TestCase

from matchpredictor.evaluation.evaluator import Evaluator
from matchpredictor.matchresults.results_provider import training_results, validation_results
from matchpredictor.predictors.linear_regression_predictor import train_regression_predictor


class TestLinearRegressionPredictor(TestCase):
    def test_accuracy(self) -> None:
        training_data = training_results('england.csv', 2019, result_filter=lambda result: result.fixture.season >= 2015)
        validation_data = validation_results('england.csv', 2019)
        predictor = train_regression_predictor(training_data)

        accuracy, _ = Evaluator(predictor).measure_accuracy(validation_data)

        self.assertGreaterEqual(accuracy, .33)
