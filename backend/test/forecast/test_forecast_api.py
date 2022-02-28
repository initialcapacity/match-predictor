from unittest import TestCase

from matchpredictor.app import app


class TestForecastApi(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_client = app.test_client()

    def test_forecast(self) -> None:
        response = self.test_client.get(
            '/forecast?home_name=Everton&home_country=england&away_name=Burnley&away_country=england'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'fixture': {
                'away_team': {'name': 'Burnley', 'country': 'england'},
                'home_team': {'name': 'Everton', 'country': 'england'},
                'tier': None
            },
            'outcome': 'home'})
