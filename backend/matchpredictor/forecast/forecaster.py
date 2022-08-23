from dataclasses import dataclass
from typing import Optional

from matchpredictor.matchresults.result import Fixture, Team, Outcome, Scenario
from matchpredictor.model.model_provider import ModelProvider


@dataclass(frozen=True)
class Forecast(object):
    fixture: Fixture
    model_name: str
    outcome: Outcome
    confidence: Optional[float]


def fixture_is_invalid(fixture: Fixture) -> bool:
    return fixture.home_team.name == fixture.away_team.name


class Forecaster:
    def __init__(self, model_provider: ModelProvider) -> None:
        self.__model_provider = model_provider

    def forecast(self, fixture: Fixture, model_name: str) -> Optional[Forecast]:
        if fixture_is_invalid(fixture):
            return None

        predictor = self.__model_provider.get_predictor(model_name)
        if predictor is None:
            return None

        prediction = predictor.predict(fixture)

        return Forecast(
            fixture=fixture,
            model_name=model_name,
            outcome=prediction.outcome,
            confidence=prediction.confidence
        )

    def forecast_in_progress(self, fixture: Fixture, scenario: Scenario, model_name: str) -> Optional[Forecast]:
        if fixture_is_invalid(fixture):
            return None

        predictor = self.__model_provider.get_in_progress_predictor(model_name)
        if predictor is None:
            return None

        prediction = predictor.predict_in_progress(fixture, scenario)

        return Forecast(
            fixture=fixture,
            model_name=model_name,
            outcome=prediction.outcome,
            confidence=prediction.confidence
        )
