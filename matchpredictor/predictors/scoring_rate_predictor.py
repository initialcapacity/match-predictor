from dataclasses import dataclass
from random import random
from typing import Iterable

from matchpredictor.predictors.predictor import Predictor
from matchpredictor.results.result import Team, Fixture, Outcome, Result


@dataclass
class TeamScoring(object):
    goals: int
    matches: int

    def goals_per_minute(self) -> float:
        if self.matches == 0:
            return 1 / 90

        return self.goals / 90 / self.matches


class ScoringRates:
    scoring_dict: dict[str, TeamScoring]

    def __init__(self):
        self.scoring_dict = {}

    def get_rate(self, team: Team) -> float:
        team_scoring = self.scoring_dict.get(team.name, TeamScoring(0, 0))

        return team_scoring.goals_per_minute()

    def add_match(self, team: Team, goals: int):
        team_scoring = self.scoring_dict.get(team.name, TeamScoring(0, 0))

        self.scoring_dict[team.name] = TeamScoring(team_scoring.goals + goals, team_scoring.matches + 1)


class ScoringRatePredictor(Predictor):
    def __init__(self, scoring_rates: ScoringRates):
        self.scoring_rates = scoring_rates

    def predict(self, fixture: Fixture) -> Outcome:
        results = [self.__simulate(fixture) for _ in range(100)]

        return max(set(results), key=results.count)

    def __simulate(self, fixture: Fixture) -> Outcome:
        home_goal_rate = self.scoring_rates.get_rate(fixture.home_team)
        away_goal_rate = self.scoring_rates.get_rate(fixture.away_team)

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


def calculate_scoring_rates(results: Iterable[Result]) -> ScoringRates:
    scoring_rates = ScoringRates()

    for result in results:
        scoring_rates.add_match(result.fixture.home_team, result.home_goals)
        scoring_rates.add_match(result.fixture.away_team, result.away_goals)

    return scoring_rates
