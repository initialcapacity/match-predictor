from unittest import TestCase

from matchpredictor.evaluation.evaluator import Evaluator
from matchpredictor.matchresults.result import Team, Fixture, Outcome, Result
from matchpredictor.matchresults.results_provider import training_results, validation_results
from matchpredictor.predictors.predictor import Prediction
from matchpredictor.predictors.simulation_predictor import train_offense_predictor, simulation_predictor
from matchpredictor.predictors.simulators.scoring_rates import ScoringRates
from matchpredictor.predictors.simulators.simulator import offense_simulator
from test.predictors import csv_location


class TestScoringRatePredictor(TestCase):
    def test_accuracy_last_two_seasons(self) -> None:
        training_data = training_results(csv_location, 2019, result_filter=lambda result: result.season >= 2017)
        validation_data = validation_results(csv_location, 2019)
        predictor = train_offense_predictor(training_data, 50)

        accuracy, _ = Evaluator(predictor).measure_accuracy(validation_data)

        self.assertGreaterEqual(accuracy, .33)

    def test_confidence(self) -> None:
        scoring_rates = ScoringRates([
            Result(
                fixture=Fixture(Team('Always Wins'), Team('Always Loses'), 'Some league'),
                outcome=Outcome.HOME,
                home_goals=90,
                away_goals=0,
                season=1999,
            )
        ])

        predictor = simulation_predictor(simulator=offense_simulator(scoring_rates), simulations=1)

        prediction = predictor(Fixture(
            home_team=Team('Always Wins'),
            away_team=Team('Always Loses'),
            league='boring league',
        ))

        self.assertEqual(Prediction(Outcome.HOME, 1), prediction)
