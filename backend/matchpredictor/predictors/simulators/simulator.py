from random import random
from typing import TypeAlias, Callable

from matchpredictor.matchresults.result import Fixture, Outcome, Scenario
from matchpredictor.predictors.simulators.scoring_rates import ScoringRates

Simulator: TypeAlias = Callable[[Fixture, Scenario], Outcome]


def offense_simulator(scoring_rates: ScoringRates) -> Simulator:
    def simulate(fixture: Fixture, scenario: Scenario) -> Outcome:
        home_goal_rate = scoring_rates.goals_scored_per_minute(fixture.home_team)
        away_goal_rate = scoring_rates.goals_scored_per_minute(fixture.away_team)

        return __outcome_from_goal_rate(home_goal_rate, away_goal_rate, scenario)

    return simulate


def offense_and_defense_simulator(scoring_rates: ScoringRates) -> Simulator:
    def simulate(fixture: Fixture, scenario: Scenario) -> Outcome:
        home_goal_rate = scoring_rates.goals_scored_per_minute(fixture.home_team)
        home_defensive_factor = scoring_rates.defensive_factor(fixture.home_team)

        away_goal_rate = scoring_rates.goals_scored_per_minute(fixture.away_team)
        away_defensive_factor = scoring_rates.defensive_factor(fixture.away_team)

        return __outcome_from_goal_rate(
            home_goal_rate * away_defensive_factor,
            away_goal_rate * home_defensive_factor,
            scenario
        )

    return simulate


def __outcome_from_goal_rate(
        home_goal_rate: float,
        away_goal_rate: float,
        scenario: Scenario,
) -> Outcome:
    home_score = scenario.home_goals
    away_score = scenario.away_goals

    for _ in range(90 - scenario.minutes_elapsed):
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
