from unittest import TestCase

from matchpredictor.matchresults.result import Team, Fixture, Outcome, Result
from matchpredictor.predictors.predictor import Prediction
from matchpredictor.predictors.simulation_predictor import SimulationPredictor
from matchpredictor.predictors.simulators.scoring_rates import ScoringRates
from matchpredictor.predictors.simulators.simulator import offense_simulator


class TestScoringRatePredictor(TestCase):
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

        predictor = SimulationPredictor(simulator=offense_simulator(scoring_rates), simulations=1)

        prediction = predictor.predict(Fixture(
            home_team=Team('Always Wins'),
            away_team=Team('Always Loses'),
            league='boring league',
        ))

        self.assertEqual(Prediction(Outcome.HOME, 1), prediction)
