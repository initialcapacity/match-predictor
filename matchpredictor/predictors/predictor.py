from abc import ABC, abstractmethod

from matchpredictor.results.result import Fixture, Outcome


class Predictor(ABC):
    @abstractmethod
    def predict(self, fixture: Fixture) -> Outcome:
        pass
