from random import random
from typing import TypeAlias, Callable

from matchpredictor.matchresults.result import Fixture, Outcome
from matchpredictor.predictors.simulators.scoring_rates import ScoringRates

Simulator: TypeAlias = Callable[[Fixture], Outcome]


def offense_simulator(scoring_rates: ScoringRates) -> Simulator:
    def simulate(fixture: Fixture) -> Outcome:
        home_goal_rate = scoring_rates.goals_scored_per_minute(fixture.home_team)
        away_goal_rate = scoring_rates.goals_scored_per_minute(fixture.away_team)

        return __outcome_from_goal_rate(home_goal_rate, away_goal_rate)

    return simulate


def offense_and_defense_simulator(scoring_rates: ScoringRates) -> Simulator:
    def simulate(fixture: Fixture) -> Outcome:
        home_goal_rate = scoring_rates.goals_scored_per_minute(fixture.home_team)
        home_defensive_factor = scoring_rates.defensive_factor(fixture.home_team)

        away_goal_rate = scoring_rates.goals_scored_per_minute(fixture.away_team)
        away_defensive_factor = scoring_rates.defensive_factor(fixture.away_team)

        return __outcome_from_goal_rate(
            home_goal_rate * away_defensive_factor,
            away_goal_rate * home_defensive_factor,
        )

    return simulate


def __outcome_from_goal_rate(home_goal_rate: float, away_goal_rate: float) -> Outcome:
    home_score = 0
    away_score = 0

    for _ in range(90):
        if random() <= home_goal_rate:
            home_score += 1
        if random() <= away_goal_rate:
            away_score += 1

    if home_score > away_score:
        return Outcome.HOME
    elif away_score > home_score:
        return Outcome.AWAY
    else:
        return Outcome.DRAW
