from matchpredictor.matchresults.result import Fixture, Outcome
from matchpredictor.predictors.predictor import Predictor


class HomePredictor(Predictor):
    def predict(self, fixture: Fixture) -> Outcome:
        return Outcome.HOME
