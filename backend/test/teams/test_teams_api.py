from typing import Dict, cast, Any
from unittest import TestCase

from matchpredictor.app import create_app


class TestTeamsApi(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_client = create_app().test_client()

    def test_list_teams(self) -> None:
        response = self.test_client.get('/teams')

        self.assertEqual(response.status_code, 200)
        teams = cast(Dict[str, Any], response.get_json())["teams"]
        self.assertIsNotNone(teams)

        self.assertTrue({'name': 'Chelsea', 'leagues': ['Barclays Premier League', 'UEFA Champions League']} in teams,
                        'Chelsea should be in teams')
        self.assertTrue({'name': 'AS Roma',
                         'leagues': ['Italy Serie A', 'UEFA Europa Conference League', 'UEFA Europa League']} in teams,
                        "Roma should be in teams")
        self.assertTrue({'name': 'VfL Wolfsburg', 'leagues': ['German Bundesliga', 'UEFA Champions League']} in teams,
                        "Wolfsburg should be in teams")

        self.assertGreater(len(teams), 100, "there likely aren't enough teams")
