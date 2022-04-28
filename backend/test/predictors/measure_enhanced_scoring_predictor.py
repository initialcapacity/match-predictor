from unittest import TestCase

from matchpredictor.evaluation.evaluator import Evaluator
from matchpredictor.matchresults.results_provider import training_results, validation_results
from matchpredictor.predictors.simulation_predictor import train_offense_and_defense_predictor
from test.predictors import csv_location


class TestEnhancedScoringPredictor(TestCase):
    def test_accuracy_last_two_seasons(self) -> None:
        training_data = training_results(csv_location, 2019, result_filter=lambda result: result.season >= 2017)
        validation_data = validation_results(csv_location, 2019)
        predictor = train_offense_and_defense_predictor(training_data, 50)

        accuracy, _ = Evaluator(predictor).measure_accuracy(validation_data)

        self.assertGreaterEqual(accuracy, .33)
