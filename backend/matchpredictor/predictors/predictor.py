from abc import ABC, abstractmethod
from typing import Dict, Optional

from matchpredictor.matchresults.result import Fixture, Outcome


class Predictor(ABC):
    @abstractmethod
    def predict(self, fixture: Fixture) -> Outcome:
        pass


class PredictorProvider:
    predictors: Dict[str, Predictor]

    def __init__(self) -> None:
        self.predictors = {}

    def add(self, league: str, predictor: Predictor) -> None:
        self.predictors[league] = predictor

    def get(self, league: str) -> Optional[Predictor]:
        return self.predictors.get(league, None)
