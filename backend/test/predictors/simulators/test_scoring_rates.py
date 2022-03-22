from unittest import TestCase

from matchpredictor.matchresults.result import Result, Fixture, Team, Outcome
from matchpredictor.predictors.simulators.scoring_rates import ScoringRates


class TestScoringRates(TestCase):
    def test(self) -> None:
        results = [
            Result(
                fixture=Fixture(
                    home_team=Team("Chelsea"),
                    away_team=Team("Liverpool"),
                    league="England"
                ),
                home_goals=4,
                away_goals=2,
                season=2022,
                outcome=Outcome.HOME
            ),
            Result(
                fixture=Fixture(
                    home_team=Team("Chelsea"),
                    away_team=Team("Burnley"),
                    league="England"
                ),
                home_goals=3,
                away_goals=3,
                season=2022,
                outcome=Outcome.DRAW
            ),
            Result(
                fixture=Fixture(
                    home_team=Team("Liverpool"),
                    away_team=Team("Burnley"),
                    league="England"
                ),
                home_goals=1,
                away_goals=5,
                season=2022,
                outcome=Outcome.AWAY
            ),
        ]

        rates = ScoringRates(results)

        self.assertEqual(2.5 / 3, rates.defensive_factor(Team("Chelsea")))
        self.assertEqual(7 / 180, rates.goals_scored_per_minute(Team("Chelsea")))

        self.assertEqual(4.5 / 3, rates.defensive_factor(Team("Liverpool")))
        self.assertEqual(3 / 180, rates.goals_scored_per_minute(Team("Liverpool")))

        self.assertEqual(2 / 3, rates.defensive_factor(Team("Burnley")))
        self.assertEqual(8 / 180, rates.goals_scored_per_minute(Team("Burnley")))

        self.assertEqual(1, rates.defensive_factor(Team("Not in the results")))
        self.assertEqual(1 / 90, rates.goals_scored_per_minute(Team("Not in the results")))
