from dataclasses import dataclass
from typing import Optional

from matchpredictor.matchresults.result import Fixture, Team, Outcome
from matchpredictor.model.model_provider import ModelProvider


@dataclass(frozen=True)
class Forecast(object):
    fixture: Fixture
    model_name: str
    outcome: Outcome
    confidence: Optional[float]


class Forecaster:
    def __init__(self, model_provider: ModelProvider) -> None:
        self.__model_provider = model_provider

    def forecast(self, home_team: Team, away_team: Team, league: str, model_name: str) -> Optional[Forecast]:
        fixture = Fixture(
            home_team=home_team,
            away_team=away_team,
            league=league,
        )

        model = self.__model_provider.get(model_name)
        if model is None:
            return None

        prediction = model.predictor.predict(fixture)

        return Forecast(
            fixture=fixture,
            model_name=model_name,
            outcome=prediction.outcome,
            confidence=prediction.confidence
        )
