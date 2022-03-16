from unittest import TestCase

from matchpredictor.matchresults.result import Result, Fixture, Team, Outcome
from matchpredictor.matchresults.results_provider import load_five_thirty_eight_spi_results


class TestResultsProvider(TestCase):

    def test_load_five_thirty_eight_spi_results(self) -> None:
        results = load_five_thirty_eight_spi_results('spi_matches_sample', 2020)

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

    def test_load_five_thirty_eight_spi_results__with_the_full_data_set(self) -> None:
        results = load_five_thirty_eight_spi_results('spi_matches', 2030)
        self.assertEqual(52119, len(results))
