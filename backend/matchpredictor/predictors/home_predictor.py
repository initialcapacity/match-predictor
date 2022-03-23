from matchpredictor.matchresults.result import Fixture, Outcome
from matchpredictor.predictors.predictor import Prediction


def home_predictor(fixture: Fixture) -> Prediction:
    return Prediction(outcome=Outcome.HOME)
