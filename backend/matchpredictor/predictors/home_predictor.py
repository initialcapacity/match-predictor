from typing import Optional, Tuple

from matchpredictor.matchresults.result import Fixture, Outcome
from matchpredictor.predictors.predictor import Predictor


class HomePredictor(Predictor):
    def predict(self, fixture: Fixture) -> Tuple[Outcome, Optional[float]]:
        return Outcome.HOME, None
