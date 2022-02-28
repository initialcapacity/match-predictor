from dataclasses import dataclass
from typing import Optional

from matchpredictor.matchresults.result import Fixture, Team, Outcome
from matchpredictor.predictors.predictor import Predictor


@dataclass(frozen=True)
class Forecast(object):
    fixture: Fixture
    outcome: Outcome


class Forecaster:
    def __init__(self, predictor: Predictor) -> None:
        self.predictor = predictor

    def forecast(self, home_team: Team, away_team: Team) -> Optional[Forecast]:
        fixture = Fixture(
            home_team=home_team,
            away_team=away_team,
        )

        outcome = self.predictor.predict(fixture)

        if outcome is None:
            return None

        return Forecast(fixture=fixture, outcome=outcome)
