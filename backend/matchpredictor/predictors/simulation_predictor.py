from typing import Optional, Tuple, Iterable

from matchpredictor.matchresults.result import Fixture, Outcome, Result
from matchpredictor.predictors.predictor import Predictor
from matchpredictor.predictors.simulators.scoring_rates import ScoringRates
from matchpredictor.predictors.simulators.simulator import Simulator, offense_simulator, offense_and_defense_simulator


class SimulationPredictor(Predictor):
    def __init__(self, simulator: Simulator, simulations: int):
        self.simulator = simulator
        self.simulations = simulations

    def predict(self, fixture: Fixture) -> Tuple[Outcome, Optional[float]]:
        results = [self.simulator(fixture) for _ in range(self.simulations)]

        home_count = sum(map(lambda r: r is Outcome.HOME, results))
        away_count = sum(map(lambda r: r is Outcome.AWAY, results))
        draw_count = sum(map(lambda r: r is Outcome.DRAW, results))

        if home_count > away_count and home_count > draw_count:
            return Outcome.HOME, home_count / self.simulations
        if away_count > draw_count:
            return Outcome.AWAY, away_count / self.simulations
        else:
            return Outcome.DRAW, draw_count / self.simulations


def train_offense_predictor(results: Iterable[Result], simulations: int) -> SimulationPredictor:
    return SimulationPredictor(offense_simulator(ScoringRates(results)), simulations)


def train_offense_and_defense_predictor(results: Iterable[Result], simulations: int) -> SimulationPredictor:
    return SimulationPredictor(offense_and_defense_simulator(ScoringRates(results)), simulations)
