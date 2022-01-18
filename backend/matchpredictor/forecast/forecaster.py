from dataclasses import dataclass
from typing import Optional

from matchpredictor.matchresults.result import Fixture, Team, Outcome
from matchpredictor.predictors.predictor import PredictorProvider


@dataclass(frozen=True)
class Forecast(object):
    fixture: Fixture
    outcome: Outcome


class Forecaster:
    def __init__(self, provider: PredictorProvider) -> None:
        self.provider = provider

    def forecast(self, league: str, home_team_name: str, away_team_name: str) -> Optional[Forecast]:
        predictor = self.provider.get(league)
        if predictor is None:
            return None

        fixture = Fixture(
            home_team=Team(home_team_name),
            away_team=Team(away_team_name),
            league=league,
        )

        outcome = predictor.predict(fixture)

        if outcome is None:
            return None

        return Forecast(fixture=fixture, outcome=outcome)
