from unittest import TestCase

from matchpredictor.evaluation.evaluator import Evaluator
from matchpredictor.matchresults.results_provider import training_results, validation_results
from matchpredictor.predictors.scoring_rate_predictor import train_scoring_predictor


class TestScoringRatePredictor(TestCase):
    def test_accuracy_last_two_seasons(self) -> None:
        training_data = training_results('england', 2019, result_filter=lambda result: result.season >= 2017)
        validation_data = validation_results('england', 2019)
        predictor = train_scoring_predictor(training_data, 50)

        accuracy, _ = Evaluator(predictor).measure_accuracy(validation_data)

        self.assertGreaterEqual(accuracy, .33)
