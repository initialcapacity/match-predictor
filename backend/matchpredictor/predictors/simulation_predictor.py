from typing import Iterable

from matchpredictor.matchresults.result import Fixture, Outcome, Result
from matchpredictor.predictors.predictor import Predictor, Prediction
from matchpredictor.predictors.simulators.scoring_rates import ScoringRates
from matchpredictor.predictors.simulators.simulator import Simulator, offense_simulator, offense_and_defense_simulator


def simulation_predictor(simulator: Simulator, simulations: int) -> Predictor:
    def predict(fixture: Fixture) -> Prediction:
        results = [simulator(fixture) for _ in range(simulations)]

        home_count = sum(map(lambda r: r is Outcome.HOME, results))
        away_count = sum(map(lambda r: r is Outcome.AWAY, results))
        draw_count = sum(map(lambda r: r is Outcome.DRAW, results))

        if home_count > away_count and home_count > draw_count:
            return Prediction(outcome=Outcome.HOME, confidence=home_count / simulations)
        if away_count > draw_count:
            return Prediction(outcome=Outcome.AWAY, confidence=away_count / simulations)
        else:
            return Prediction(outcome=Outcome.DRAW, confidence=draw_count / simulations)

    return predict


def train_offense_predictor(results: Iterable[Result], simulations: int) -> Predictor:
    return simulation_predictor(offense_simulator(ScoringRates(results)), simulations)


def train_offense_and_defense_predictor(results: Iterable[Result], simulations: int) -> Predictor:
    return simulation_predictor(offense_and_defense_simulator(ScoringRates(results)), simulations)
