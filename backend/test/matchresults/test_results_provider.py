from unittest import TestCase

import responses

from matchpredictor.matchresults.result import Result, Fixture, Team, Outcome
from matchpredictor.matchresults.results_provider import load_results

spi_matches_sample_csv = """season,date,league_id,league,team1,team2,spi1,spi2,prob1,prob2,probtie,proj_score1,proj_score2,importance1,importance2,score1,score2,xg1,xg2,nsxg1,nsxg2,adj_score1,adj_score2
2016,2016-07-09,7921,FA Women's Super League,Liverpool Women,Reading,51.56,50.42,0.4389,0.2767,0.2844,1.39,1.05,,,2,1,,,,,,
2016,2016-07-17,7921,FA Women's Super League,Chelsea FC Women,Arsenal Women,59.43,60.99,0.4124,0.3157,0.2719,1.45,1.24,,,1,2,,,,,,
2016,2016-07-10,7921,FA Women's Super League,Chelsea FC Women,Birmingham City,59.85,54.64,0.4799,0.2487,0.2714,1.53,1.03,,,1,1,,,,,,
"""

spi_matches_error_sample_csv = """season,date,league_id,league,team1,team2,spi1,spi2,prob1,prob2,probtie,proj_score1,proj_score2,importance1,importance2,score1,score2,xg1,xg2,nsxg1,nsxg2,adj_score1,adj_score2
2016,2016-07-09,7921,FA Women's Super League,Liverpool Women,Reading,51.56,50.42,0.4389,0.2767,0.2844,1.39,1.05,,,ABC,DEF,,,,,,
this,row,is,invalid,
"""


class TestResultsProvider(TestCase):

    @responses.activate
    def test_load_five_thirty_eight_spi_results(self) -> None:

        responses.add(
            method='GET',
            url='https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv',
            body=spi_matches_sample_csv,
            status=200,
        )

        results = load_results('spi_matches')

        recorded_calls = responses.calls
        self.assertEqual(1, len(recorded_calls))

        expected_first_result = Result(
            fixture=Fixture(
                home_team=Team(name='Liverpool Women'),
                away_team=Team(name='Reading'),
                league="FA Women's Super League",
            ),
            outcome=Outcome.HOME,
            home_goals=2,
            away_goals=1,
            season=2016,
        )

        self.assertEqual(3, len(results))
        self.assertEqual(expected_first_result, results[0])
        self.assertEqual(Outcome.AWAY, results[1].outcome)
        self.assertEqual(Outcome.DRAW, results[2].outcome)

    @responses.activate
    def test_filtering_results(self) -> None:

        responses.add(
            method='GET',
            url='https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv',
            body=spi_matches_sample_csv,
            status=200,
        )

        def only_chelsea(result: Result) -> bool:
            return result.fixture.home_team.name == 'Chelsea FC Women'

        results = load_results('spi_matches', only_chelsea)

        self.assertEqual(2, len(results))
        self.assertEqual(Team('Chelsea FC Women'), results[0].fixture.home_team)
        self.assertEqual(Team('Chelsea FC Women'), results[1].fixture.home_team)

    @responses.activate
    def test_error_handling_on_csv_parse_error(self) -> None:

        responses.add(
            method='GET',
            url='https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv',
            body=spi_matches_error_sample_csv,
            status=200,
        )

        results = load_results('spi_matches')

        self.assertEqual(0, len(results))

    @responses.activate
    def test_error_handling_on_csv_download_error(self) -> None:

        responses.add(
            method='GET',
            url='https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv',
            body='',
            status=500,
        )

        caught_exception = None

        try:
            load_results('spi_matches')
        except Exception as e:
            caught_exception = e

        self.assertIsNotNone(caught_exception)
