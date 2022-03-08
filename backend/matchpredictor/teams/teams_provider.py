from dataclasses import dataclass
from typing import List, Dict, Set, Optional

from matchpredictor.matchresults.result import Fixture, Team


@dataclass(frozen=True)
class TeamWithLeagues(object):
    name: str
    leagues: List[str]


class TeamsProvider:

    def __init__(self, fixtures: List[Fixture]) -> None:
        self.fixtures = fixtures

    def all(self) -> List[TeamWithLeagues]:
        teams: Dict[str, Set[str]] = {}

        def add_team(team: Team, league: str) -> None:
            if team.name in teams:
                teams[team.name].add(league)
            else:
                teams[team.name] = {league}

        for fixture in self.fixtures:
            add_team(fixture.home_team, fixture.league)
            add_team(fixture.away_team, fixture.league)

        return [TeamWithLeagues(name=k, leagues=sorted(list(v))) for k, v in teams.items()]
