from unittest import TestCase

from matchpredictor.evaluation.evaluator import Evaluator
from matchpredictor.matchresults.results_provider import load_results
from matchpredictor.predictors.past_results_predictor import train_results_predictor


class TestPastResultsPredictor(TestCase):
    def test_accuracy(self):
        training_data = load_results('england-training.csv')
        validation_data = load_results('england-validation.csv')
        predictor = train_results_predictor(training_data)

        accuracy = Evaluator(predictor).measure_accuracy(validation_data)

        self.assertGreaterEqual(accuracy, .33)

    def test_accuracy_last_two_seasons(self):
        training_data = load_results('england-training.csv', result_filter=lambda result: result.fixture.season >= 2017)
        validation_data = load_results('england-validation.csv')
        predictor = train_results_predictor(training_data)

        accuracy = Evaluator(predictor).measure_accuracy(validation_data)

        self.assertGreaterEqual(accuracy, .33)
