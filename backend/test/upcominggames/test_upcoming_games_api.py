from unittest import TestCase

import responses

from matchpredictor.app import create_app
from test.test_builders import build_app_environment


class TestUpcomingGamesApi(TestCase):

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

        app_environment = build_app_environment(football_data_api_key='my-api-key')
        app = create_app(app_environment)
        app.config['TESTING'] = True
        self.test_client = app.test_client()

    @responses.activate
    def test_list(self) -> None:
        sample_football_data_response = """{
            "matches": [
                {
                    "area": {
                        "name": "Netherlands",
                        "code": "NLD"
                    },
                    "competition": {
                        "name": "Eredivisie",
                        "code": "DED",
                        "type": "LEAGUE"
                    },
                    "homeTeam": {
                        "name": "FC Groningen",
                        "shortName": "Groningen",
                        "tla": "GRO"
                    },
                    "awayTeam": {
                        "name": "AFC Ajax",
                        "shortName": "Ajax",
                        "tla": "AJA"
                    }
                },
                {
                    "area": {
                        "name": "England",
                        "code": "ENG"
                    },
                    "competition": {
                        "name": "Championship",
                        "code": "ELC",
                        "type": "LEAGUE"
                    },
                    "homeTeam": {
                        "name": "Luton Town FC",
                        "shortName": "Luton Town",
                        "tla": "LUT"
                    },
                    "awayTeam": {
                        "name": "Sunderland AFC",
                        "shortName": "Sunderland",
                        "tla": "SUN"
                    }
                }
            ]
        }
        """

        responses.add(
            method='GET',
            url='https://api.football-data.org/v4/matches?dateFrom=2023-06-01&dateTo=2023-06-10',
            status=200,
            body=sample_football_data_response
        )

        response = self.test_client.get('/upcoming-games/2023-06-01')

        expected_body = {
            "games": [
                {
                    "league": "Dutch Eredivisie",
                    "home": "Groningen",
                    "away": "Ajax",
                },
                {
                    "league": "English League Championship",
                    "home": "Luton Town",
                    "away": "Sunderland",
                },
            ]
        }

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_body, response.get_json())

        self.assertEqual(1, len(responses.calls))

        recorded_request = responses.calls[0].request
        self.assertEqual('my-api-key', recorded_request.headers['X-Auth-Token'])

    @responses.activate
    def test_list__with_no_mapping_for_the_league(self) -> None:
        sample_football_data_response = """{
                    "matches": [
                        {
                            "area": {
                                "name": "MiddleEarth",
                                "code": "MID"
                            },
                            "competition": {
                                "name": "BattleForTheRing",
                                "code": "BFR",
                                "type": "LEAGUE"
                            },
                            "homeTeam": {
                                "name": "Gondor",
                                "shortName": "Gondor",
                                "tla": "GON"
                            },
                            "awayTeam": {
                                "name": "The Shire FC",
                                "shortName": "The Shire",
                                "tla": "TSH"
                            }
                        }
                    ]
                }
                """

        responses.add(
            method='GET',
            url='https://api.football-data.org/v4/matches?dateFrom=2023-06-01&dateTo=2023-06-10',
            status=200,
            body=sample_football_data_response
        )

        response = self.test_client.get('/upcoming-games/2023-06-01')

        expected_body = {
            "games": [
                {
                    "league": "MiddleEarth BattleForTheRing",
                    "home": "Gondor",
                    "away": "The Shire",
                }
            ]
        }

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_body, response.get_json())

    def test_list__when_date_is_invalid(self) -> None:
        response = self.test_client.get('/upcoming-games/this-is-not-a-date')
        self.assertEqual(400, response.status_code)

    @responses.activate
    def test_list__with_unexpected_json_from_football_data(self) -> None:

        responses.add(
            method='GET',
            url='https://api.football-data.org/v4/matches?dateFrom=2023-06-01&dateTo=2023-06-10',
            status=200,
            body="{\"hello\":\"world\"}"
        )

        response = self.test_client.get('/upcoming-games/2023-06-01')

        self.assertEqual(503, response.status_code)

    @responses.activate
    def test_list__with_invalid_json(self) -> None:

        responses.add(
            method='GET',
            url='https://api.football-data.org/v4/matches?dateFrom=2023-06-01&dateTo=2023-06-10',
            status=200,
            body="this is not json"
        )

        response = self.test_client.get('/upcoming-games/2023-06-01')

        self.assertEqual(503, response.status_code)
