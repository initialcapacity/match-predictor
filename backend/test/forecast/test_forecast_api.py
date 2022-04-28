from unittest import TestCase

import responses

from matchpredictor.app import create_app


class TestForecastApi(TestCase):
    @responses.activate
    def setUp(self) -> None:
        super().setUp()

        responses.add(
            method='GET',
            url='https://example.com/some.csv',
            status=200,
            body="""season,date,league_id,league,team1,team2,spi1,spi2,prob1,prob2,probtie,proj_score1,proj_score2,importance1,importance2,score1,score2,xg1,xg2,nsxg1,nsxg2,adj_score1,adj_score2
2020,2020-11-13,0000,Test League,Always Wins,Always Loses,65.59,39.99,0.7832,0.0673,0.1495,2.58,0.62,77.1,28.8,90,0,0.49,0.45,1.05,0.75,3.15,0.0"""
        )

        app = create_app('https://example.com/some.csv')
        self.test_client = app.test_client()

    def test_forecast(self) -> None:
        response = self.test_client.get(
            '/forecast?home_name=Always+Wins&away_name=Always+Loses&league=Test+League'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'fixture': {
                'away_team': {'name': 'Always Loses'},
                'home_team': {'name': 'Always Wins'},
                'league': 'Test League'
            },
            'outcome': 'home',
            'confidence': 1
        })
