from random import random
from typing import Iterable, Tuple, Optional

from matchpredictor.matchresults.result import Result, Fixture, Outcome
from matchpredictor.predictors.predictor import Predictor
from matchpredictor.predictors.scoring_rates import ScoringRates


class EnhancedScoringPredictor(Predictor):
    def __init__(self, scoring_rates: ScoringRates, simulations: int):
        self.scoring_rates = scoring_rates
        self.simulations = simulations

    def predict(self, fixture: Fixture) -> Tuple[Outcome, Optional[float]]:
        results = [self.__simulate(fixture) for _ in range(self.simulations)]

        home_count = sum(map(lambda r: r is Outcome.HOME, results))
        away_count = sum(map(lambda r: r is Outcome.AWAY, results))
        draw_count = sum(map(lambda r: r is Outcome.DRAW, results))

        if home_count > away_count and home_count > draw_count:
            return Outcome.HOME, home_count / self.simulations
        if away_count > draw_count:
            return Outcome.AWAY, away_count / self.simulations
        else:
            return Outcome.DRAW, draw_count / self.simulations

    def __simulate(self, fixture: Fixture) -> Outcome:
        home_goal_rate = self.scoring_rates.goals_scored_per_minute(fixture.home_team)
        home_defensive_factor = self.scoring_rates.defensive_factor(fixture.home_team)
        home_score = 0

        away_goal_rate = self.scoring_rates.goals_scored_per_minute(fixture.away_team)
        away_defensive_factor = self.scoring_rates.defensive_factor(fixture.away_team)
        away_score = 0

        for _ in range(90):
            if random() <= home_goal_rate * away_defensive_factor:
                home_score += 1
            if random() <= away_goal_rate * home_defensive_factor:
                away_score += 1

        if home_score > away_score:
            return Outcome.HOME
        elif away_score > home_score:
            return Outcome.AWAY
        else:
            return Outcome.DRAW


def train_enhanced_scoring_predictor(results: Iterable[Result], simulations: int) -> EnhancedScoringPredictor:
    return EnhancedScoringPredictor(ScoringRates(results), simulations)
