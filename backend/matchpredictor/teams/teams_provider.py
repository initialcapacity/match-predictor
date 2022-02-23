from typing import List

from matchpredictor.matchresults.result import Fixture, Team


class TeamsProvider:

    def __init__(self, fixtures: List[Fixture]) -> None:
        self.fixtures = fixtures

    def unique_teams(self) -> set[Team]:
        teams = set()

        for fixture in self.fixtures:
            teams.add(fixture.home_team)
            teams.add(fixture.away_team)

        return teams

