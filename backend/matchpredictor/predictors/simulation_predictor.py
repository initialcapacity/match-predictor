from typing import Iterable

from matchpredictor.matchresults.result import Fixture, Outcome, Result, Scenario
from matchpredictor.predictors.predictor import Predictor, Prediction, InProgressPredictor
from matchpredictor.predictors.simulators.scoring_rates import ScoringRates
from matchpredictor.predictors.simulators.simulator import Simulator, offense_simulator, offense_and_defense_simulator


class SimulationPredictor(InProgressPredictor):
    def __init__(self, simulator: Simulator, simulations: int) -> None:
        self.simulator = simulator
        self.simulations = simulations

    def predict(self, fixture: Fixture) -> Prediction:
        return self.predict_in_progress(fixture, Scenario(0, 0, 0))

    def predict_in_progress(self, fixture: Fixture, scenario: Scenario) -> Prediction:
        results = [self.simulator(fixture, scenario) for _ in range(self.simulations)]

        home_count = sum(map(lambda r: r is Outcome.HOME, results))
        away_count = sum(map(lambda r: r is Outcome.AWAY, results))
        draw_count = sum(map(lambda r: r is Outcome.DRAW, results))

        if home_count > away_count and home_count > draw_count:
            return Prediction(outcome=Outcome.HOME, confidence=home_count / self.simulations)
        if away_count > draw_count:
            return Prediction(outcome=Outcome.AWAY, confidence=away_count / self.simulations)
        else:
            return Prediction(outcome=Outcome.DRAW, confidence=draw_count / self.simulations)


def train_offense_predictor(results: Iterable[Result], simulations: int) -> Predictor:
    return SimulationPredictor(offense_simulator(ScoringRates(results)), simulations)


def train_offense_and_defense_predictor(results: Iterable[Result], simulations: int) -> Predictor:
    return SimulationPredictor(offense_and_defense_simulator(ScoringRates(results)), simulations)
