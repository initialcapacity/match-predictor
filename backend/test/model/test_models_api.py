from unittest import TestCase

import responses

from matchpredictor.app import create_app
from test.test_builders import build_app_environment


class TestModelsApi(TestCase):
    @responses.activate
    def setUp(self) -> None:
        super().setUp()

        responses.add(
            method='GET',
            url='https://example.com/some.csv',
            status=200,
            body="""season,date,league_id,league,team1,team2,spi1,spi2,prob1,prob2,probtie,proj_score1,proj_score2,importance1,importance2,score1,score2,xg1,xg2,nsxg1,nsxg2,adj_score1,adj_score2
                2021,2021-08-11,2411,Barclays Premier League,Manchester United,Chelsea,79.99,85.88,0.3664,0.3843,0.2494,1.48,1.52,53.5,61.0,4,0,2.34,1.27,1.36,1.29,3.92,0.0
                2021,2021-09-17,1818,UEFA Champions League,Chelsea,Valencia,84.04,76.67,0.5901,0.1932,0.2167,1.93,1.01,81.3,85.8,0,1,3.11,0.88,2.44,0.72,0.0,1.05"""
        )

        app = create_app(build_app_environment())
        self.test_client = app.test_client()

    def test_list_models(self) -> None:
        response = self.test_client.get('/models')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.get_json(), {'models': [
            {"name": "Home", "predicts_in_progress": False},
            {"name": "Points", "predicts_in_progress": False},
            {"name": "Offense simulator (fast)", "predicts_in_progress": True},
            {"name": "Offense simulator", "predicts_in_progress": True},
            {"name": "Full simulator (fast)", "predicts_in_progress": True},
            {"name": "Full simulator", "predicts_in_progress": True},
            # {"name": "Linear regression", "predicts_in_progress": False},
        ]})
