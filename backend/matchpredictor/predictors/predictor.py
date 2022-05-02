from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from matchpredictor.matchresults.result import Fixture, Outcome


@dataclass
class Prediction:
    outcome: Outcome
    confidence: Optional[float] = None


class Predictor(ABC):
    @abstractmethod
    def predict(self, fixture: Fixture) -> Prediction:
        pass
