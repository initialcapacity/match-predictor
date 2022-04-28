from dataclasses import dataclass
from typing import Optional

from matchpredictor.matchresults.result import Fixture, Team, Outcome
from matchpredictor.predictors.predictor import Predictor


@dataclass(frozen=True)
class Forecast(object):
    fixture: Fixture
    outcome: Outcome
    confidence: Optional[float]


class Forecaster:
    def __init__(self, predictor: Predictor) -> None:
        self.predictor = predictor

    def forecast(self, home_team: Team, away_team: Team, league: str) -> Optional[Forecast]:
        fixture = Fixture(
            home_team=home_team,
            away_team=away_team,
            league=league,
        )

        prediction = self.predictor(fixture)

        return Forecast(fixture=fixture, outcome=prediction.outcome, confidence=prediction.confidence)
