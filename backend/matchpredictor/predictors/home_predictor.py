from matchpredictor.matchresults.result import Fixture, Outcome
from matchpredictor.predictors.predictor import Prediction, Predictor


class HomePredictor(Predictor):
    def predict(self, fixture: Fixture) -> Prediction:
        return Prediction(outcome=Outcome.HOME)
