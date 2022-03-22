from dataclasses import dataclass
from typing import Dict, Iterable

from matchpredictor.matchresults.result import Team, Result


@dataclass
class TeamScoring(object):
    goal_scored: int
    goals_conceded: int
    matches: int

    def goals_scored_per_minute(self) -> float:
        if self.matches == 0:
            return 1 / 90

        return self.goal_scored / 90 / self.matches

    def goals_conceded_per_match(self) -> float:
        if self.matches == 0:
            return 1

        return self.goals_conceded / self.matches


class ScoringRates:
    scoring_dict: Dict[Team, TeamScoring]
    total_goals: int
    total_matches: int

    def __init__(self, results: Iterable[Result]) -> None:
        self.scoring_dict = {}
        self.total_goals = 0
        self.total_matches = 0

        for result in results:
            self.__add_result(result)

    def defensive_factor(self, team: Team) -> float:
        if team not in self.scoring_dict.keys():
            return 1

        team_scoring = self.scoring_dict.get(team, TeamScoring(0, 0, 0))
        goals_conceded_per_match = self.__global_goals_per_match() / 2

        return team_scoring.goals_conceded_per_match() / goals_conceded_per_match

    def goals_scored_per_minute(self, team: Team) -> float:
        team_scoring = self.scoring_dict.get(team, TeamScoring(0, 0, 0))

        return team_scoring.goals_scored_per_minute()

    def __add_result(self, result: Result) -> None:
        home_team_scoring = self.scoring_dict.get(result.fixture.home_team, TeamScoring(0, 0, 0))
        self.scoring_dict[result.fixture.home_team] = TeamScoring(
            goal_scored=home_team_scoring.goal_scored + result.home_goals,
            goals_conceded=home_team_scoring.goals_conceded + result.away_goals,
            matches=home_team_scoring.matches + 1,
        )

        away_team_scoring = self.scoring_dict.get(result.fixture.away_team, TeamScoring(0, 0, 0))
        self.scoring_dict[result.fixture.away_team] = TeamScoring(
            goal_scored=away_team_scoring.goal_scored + result.away_goals,
            goals_conceded=away_team_scoring.goals_conceded + result.home_goals,
            matches=away_team_scoring.matches + 1,
        )

        self.total_goals += (result.home_goals + result.away_goals)
        self.total_matches += 1

    def __global_goals_per_match(self) -> float:
        return self.total_goals / self.total_matches
