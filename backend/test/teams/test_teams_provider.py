from unittest import TestCase

from matchpredictor.matchresults.result import Team, Fixture
from matchpredictor.teams.teams_provider import TeamsProvider, TeamWithLeagues


class TestTeamsProvider(TestCase):
    def test_all(self) -> None:
        team_one = Team("Chelsea")
        team_two = Team("Roma")
        team_three = Team("Other team")
        fixtures = [
            Fixture(team_one, team_two, "japan 2"),
            Fixture(team_one, team_three, "japan 1"),
            Fixture(team_two, team_three, "japan 1")
        ]
        team_provider = TeamsProvider(fixtures)

        teams = team_provider.all()

        self.assertEqual(teams, [
            TeamWithLeagues(name='Chelsea', leagues=['japan 1', 'japan 2']),
            TeamWithLeagues(name='Roma', leagues=['japan 1', 'japan 2']),
            TeamWithLeagues(name='Other team', leagues=['japan 1']),
        ])
