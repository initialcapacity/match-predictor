from unittest import TestCase

import responses

from matchpredictor.app import create_app

spi_matches_sample_csv = """season,date,league_id,league,team1,team2,spi1,spi2,prob1,prob2,probtie,proj_score1,proj_score2,importance1,importance2,score1,score2,xg1,xg2,nsxg1,nsxg2,adj_score1,adj_score2
2021,,,Test League,Always Wins,Always Loses,,,,,,,,,,1000,0,,,,,,
"""


class TestForecastApi(TestCase):

    @responses.activate
    def test_forecast(self) -> None:
        responses.add(
            method='GET',
            url='https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv',
            body=spi_matches_sample_csv,
            status=200,
        )

        self.test_client = create_app().test_client()

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
