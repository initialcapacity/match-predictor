from unittest import TestCase

import responses

from matchpredictor.matchresults.result import Result, Fixture, Team, Outcome
from matchpredictor.matchresults.results_provider import load_results


class TestResultsProvider(TestCase):
    @responses.activate
    def test_load_five_thirty_eight_spi_results(self) -> None:
        responses.add(
            method='GET',
            url='https://example.com/some.csv',
            status=200,
            body="""season,date,league_id,league,team1,team2,spi1,spi2,prob1,prob2,probtie,proj_score1,proj_score2,importance1,importance2,score1,score2,xg1,xg2,nsxg1,nsxg2,adj_score1,adj_score2
2016,2016-07-09,7921,FA Women's Super League,Liverpool Women,Reading,51.56,50.42,0.4389,0.2767,0.2844,1.39,1.05,,,2,0,,,,,,
2016,2016-07-17,7921,FA Women's Super League,Chelsea FC Women,Arsenal Women,59.43,60.99,0.4124,0.3157,0.2719,1.45,1.24,,,1,2,,,,,,
2016,2016-07-10,7921,FA Women's Super League,Chelsea FC Women,Birmingham City,59.85,54.64,0.4799,0.2487,0.2714,1.53,1.03,,,1,1,,,,,,"""
        )

        results = load_results('https://example.com/some.csv', lambda r: r.season < 2020)

        expected_first_result = Result(
            fixture=Fixture(
                home_team=Team(name='Liverpool Women'),
                away_team=Team(name='Reading'),
                league="FA Women's Super League",
            ),
            outcome=Outcome.HOME,
            home_goals=2,
            away_goals=0,
            season=2016,
        )

        self.assertEqual(3, len(results))
        self.assertEqual(expected_first_result, results[0])
        self.assertEqual(Outcome.AWAY, results[1].outcome)
        self.assertEqual(Outcome.DRAW, results[2].outcome)

    @responses.activate
    def test_load_five_thirty_eight_spi_results_error(self) -> None:
        responses.add(
            method='GET',
            url='https://example.com/some.csv',
            status=500,
        )

        results = load_results('https://example.com/some.csv', lambda r: r.season < 2020)

        self.assertEqual(0, len(results))

    @responses.activate
    def test_load_five_thirty_eight_spi_results_parse_error(self) -> None:
        responses.add(
            method='GET',
            url='https://example.com/some.csv',
            status=200,
            body="""some error message
            with multiple lines"""
        )

        results = load_results('https://example.com/some.csv', lambda r: r.season < 2020)

        self.assertEqual(0, len(results))

