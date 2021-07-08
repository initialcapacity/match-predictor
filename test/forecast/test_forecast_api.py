from unittest import TestCase

from app import app


class TestForecastApi(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_client = app.test_client()

    def test_forecast(self):
        response = self.test_client.get('/forecast/england/2020?home_team=Everton&away_team=Burnley"')

        self.assertEqual(response.get_json(), {"outcome": "home"})
