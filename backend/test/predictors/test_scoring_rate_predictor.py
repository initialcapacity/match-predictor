from unittest import TestCase

from matchpredictor.evaluation.evaluator import Evaluator
from matchpredictor.matchresults.result import Team, Fixture, Outcome
from matchpredictor.matchresults.results_provider import training_results, validation_results
from matchpredictor.predictors.scoring_rate_predictor import train_scoring_predictor, ScoringRatePredictor, TeamScoring, \
    ScoringRates


class TestScoringRatePredictor(TestCase):
    def test_accuracy_last_two_seasons(self) -> None:
        training_data = training_results('england', 2019, result_filter=lambda result: result.season >= 2017)
        validation_data = validation_results('england', 2019)
        predictor = train_scoring_predictor(training_data, 50)

        accuracy, _ = Evaluator(predictor).measure_accuracy(validation_data)

        self.assertGreaterEqual(accuracy, .33)

    def test_confidence(self) -> None:
        scoring_rates = ScoringRates()
        scoring_rates.add_match(Team('Always Wins'), 90)
        scoring_rates.add_match(Team('Always Loses'), 0)

        predictor = ScoringRatePredictor(scoring_rates=scoring_rates, simulations=1)

        outcome, confidence = predictor.predict(Fixture(
            home_team=Team('Always Wins'),
            away_team=Team('Always Loses'),
            league='boring league',
        ))

        self.assertEqual(outcome, Outcome.HOME)
        self.assertEqual(confidence, 1)
