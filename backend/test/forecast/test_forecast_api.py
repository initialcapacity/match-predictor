from unittest import TestCase

import responses

from matchpredictor.app import create_app
from test.test_builders import build_app_environment


class TestForecastApi(TestCase):
    @responses.activate
    def setUp(self) -> None:
        super().setUp()

        responses.add(
            method='GET',
            url='https://example.com/some.csv',
            status=200,
            body="""season,date,league_id,league,team1,team2,spi1,spi2,prob1,prob2,probtie,proj_score1,proj_score2,importance1,importance2,score1,score2,xg1,xg2,nsxg1,nsxg2,adj_score1,adj_score2
2021,2020-11-13,0000,Test League,Always Scores,Rarely Scores,65.59,39.99,0.7832,0.0673,0.1495,2.58,0.62,77.1,28.8,90,0,0.49,0.45,1.05,0.75,3.15,0.0
2021,2020-11-14,0000,Test League,Other,Another,65.59,39.99,0.7832,0.0673,0.1495,2.58,0.62,77.1,28.8,1,1,0.49,0.45,1.05,0.75,3.15,0.0"""
        )

        app = create_app(build_app_environment())
        self.test_client = app.test_client()

    def test_forecast_full_simulator_model(self) -> None:
        response = self.test_client.get(
            '/forecast?home_name=Rarely+Scores&away_name=Always+Scores&league=Test+League&model_name=Full+simulator'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'fixture': {
                'away_team': {'name': 'Always Scores'},
                'home_team': {'name': 'Rarely Scores'},
                'league': 'Test League'
            },
            'model_name': 'Full simulator',
            'outcome': 'away',
            'confidence': 1
        })

    def test_forecast_home_model(self) -> None:
        response = self.test_client.get(
            '/forecast?home_name=Rarely+Scores&away_name=Always+Scores&league=Test+League&model_name=Home'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'fixture': {
                'away_team': {'name': 'Always Scores'},
                'home_team': {'name': 'Rarely Scores'},
                'league': 'Test League'
            },
            'model_name': 'Home',
            'outcome': 'home',
            'confidence': None
        })

    def test_forecast_bad_model(self) -> None:
        response = self.test_client.get(
            '/forecast?home_name=Rarely+Scores&away_name=Always+Scores&league=Test+League&model_name=Bad+model'
        )

        self.assertEqual(response.status_code, 400)

    def test_forecast_in_progress(self) -> None:
        response = self.test_client.get(
            '/forecast-in-progress'
            '?home_name=Rarely+Scores'
            '&away_name=Always+Scores'
            '&league=Test+League'
            '&model_name=Full+simulator'
            '&minutes_elapsed=89'
            '&home_goals=3'
            '&away_goals=0'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'fixture': {
                'away_team': {'name': 'Always Scores'},
                'home_team': {'name': 'Rarely Scores'},
                'league': 'Test League'
            },
            'model_name': 'Full simulator',
            'outcome': 'home',
            'confidence': 1
        })

    def test_forecast_in_progress_wrong_model(self) -> None:
        response = self.test_client.get(
            '/forecast-in-progress'
            '?home_name=Rarely+Scores'
            '&away_name=Always+Scores'
            '&league=Test+League'
            '&model_name=Linear+regression'
            '&minutes_elapsed=89'
            '&home_goals=3'
            '&away_goals=0'
        )

        self.assertEqual(response.status_code, 400)
