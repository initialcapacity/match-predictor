from abc import ABC, abstractmethod
from typing import Optional, Tuple

from matchpredictor.matchresults.result import Fixture, Outcome


class Predictor(ABC):
    @abstractmethod
    def predict(self, fixture: Fixture) -> Tuple[Outcome, Optional[float]]:
        pass
