from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from matchpredictor.matchresults.result import Fixture, Outcome, Scenario


@dataclass
class Prediction:
    outcome: Outcome
    confidence: Optional[float] = None


class Predictor(ABC):
    @abstractmethod
    def predict(self, fixture: Fixture) -> Prediction:
        pass


class InProgressPredictor(Predictor):
    @abstractmethod
    def predict_in_progress(self, fixture: Fixture, scenario: Scenario) -> Prediction:
        pass
