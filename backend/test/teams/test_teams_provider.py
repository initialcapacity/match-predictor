from unittest import TestCase

from matchpredictor.matchresults.result import Team, Fixture
from matchpredictor.teams.teams_provider import TeamsProvider


class TestTeamsProvider(TestCase):
    def test_unique_teams(self) -> None:
        team_one = Team("Chelsea")
        team_two = Team("Roma")
        team_three = Team("Other team")
        fixtures = [Fixture(team_one, team_two), Fixture(team_one, team_three)]
        team_provider = TeamsProvider(fixtures)
        teams = team_provider.unique_teams()

        self.assertTrue(team_one in teams)
        self.assertTrue(team_two in teams)
        self.assertTrue(team_three in teams)
        self.assertEqual(len(teams), 3)
