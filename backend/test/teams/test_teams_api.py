from unittest import TestCase

from matchpredictor.app import app


class TestTeamsApi(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_client = app.test_client()

    def test_list_teams(self) -> None:
        response = self.test_client.get('/teams')

        self.assertEqual(response.status_code, 200)
        teams = response.get_json()["teams"]
        self.assertIsNotNone(teams)
        self.assertTrue('Chelsea' in teams, "Chelsea should be in teams")
        self.assertTrue('AS Roma' in teams, "Roma should be in teams")
        self.assertTrue('VfB Stuttgart' in teams, "Stuttgart should be in teams")
        self.assertGreater(len(teams), 100, "there likely aren't enough teams")
