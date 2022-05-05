from unittest import TestCase

from matchpredictor.matchresults.result import Team, Fixture, Outcome, Result, Scenario
from matchpredictor.predictors.predictor import Prediction
from matchpredictor.predictors.simulation_predictor import SimulationPredictor
from matchpredictor.predictors.simulators.scoring_rates import ScoringRates
from matchpredictor.predictors.simulators.simulator import offense_simulator


class TestScoringRatePredictor(TestCase):
    scoring_rates = ScoringRates([
        Result(
            fixture=Fixture(Team('Scores a lot'), Team('Not so good'), 'Some league'),
            outcome=Outcome.HOME,
            home_goals=90,
            away_goals=0,
            season=1999,
        )
    ])

    predictor = SimulationPredictor(simulator=offense_simulator(scoring_rates), simulations=1)

    def test_confidence(self) -> None:
        prediction = self.predictor.predict(Fixture(
            home_team=Team('Scores a lot'),
            away_team=Team('Not so good'),
            league='boring league',
        ))

        self.assertEqual(Prediction(Outcome.HOME, 1), prediction)

    def test_in_progress(self) -> None:
        prediction = self.predictor.predict_in_progress(Fixture(
            home_team=Team('Scores a lot'),
            away_team=Team('Not so good'),
            league='boring league',
        ), Scenario(
            minutes_elapsed=89,
            home_goals=0,
            away_goals=4,
        ))

        self.assertEqual(Prediction(Outcome.AWAY, 1), prediction)
