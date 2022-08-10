from typing import Dict, cast, Any
from unittest import TestCase

import responses

from matchpredictor.app import create_app
from test.test_builders import build_app_environment


class TestTeamsApi(TestCase):
    @responses.activate
    def setUp(self) -> None:
        super().setUp()

        responses.add(
            method='GET',
            url='https://example.com/some.csv',
            status=200,
            body="""season,date,league_id,league,team1,team2,spi1,spi2,prob1,prob2,probtie,proj_score1,proj_score2,importance1,importance2,score1,score2,xg1,xg2,nsxg1,nsxg2,adj_score1,adj_score2
                2021,2021-08-11,2411,Barclays Premier League,Manchester United,Chelsea,79.99,85.88,0.3664,0.3843,0.2494,1.48,1.52,53.5,61.0,4,0,2.34,1.27,1.36,1.29,3.92,0.0
                2021,2021-09-17,1818,UEFA Champions League,Chelsea,Valencia,84.04,76.67,0.5901,0.1932,0.2167,1.93,1.01,81.3,85.8,0,1,3.11,0.88,2.44,0.72,0.0,1.05
                2021,2021-09-19,1820,UEFA Europa League,AS Roma,Istanbul Basaksehir,71.63,52.63,0.6513,0.1293,0.2193,1.99,0.75,80.0,79.5,4,0,2.31,0.66,2.05,1.13,3.67,0.0
                2021,2021-09-22,1854,Italy Serie A,Bologna,AS Roma,63.53,72.31,0.3236,0.4214,0.2551,1.39,1.62,29.4,51.7,1,2,1.42,1.29,0.7,2.66,1.05,2.1
                2022,2022-09-16,10281,UEFA Europa Conference League,AS Roma,CSKA Sofia,72.57,45.8,0.7006,0.0926,0.2068,1.92,0.53,,,5,1,3.21,0.35,1.56,0.53,4.31,1.05
                2022,2022-09-19,1845,German Bundesliga,VfL Wolfsburg,Eintracht Frankfurt,76.16,69.65,0.5101,0.2323,0.2576,1.65,1.03,60.5,30.2,1,1,1.87,0.3,1.8,0.75,1.05,1.05
                2022,2022-09-29,1818,UEFA Champions League,VfL Wolfsburg,Sevilla FC,75.09,80.37,0.3721,0.3358,0.2921,1.1,1.03,86.9,83.8,1,1,1.27,1.1,0.96,1.02,1.05,0.84
"""
        )

        app = create_app(build_app_environment())
        self.test_client = app.test_client()

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

        self.assertEqual(len(teams), 10)
