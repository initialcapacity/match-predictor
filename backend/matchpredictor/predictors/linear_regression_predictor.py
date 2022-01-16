from typing import List, Tuple

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder

from matchpredictor.matchresults.result import Fixture, Outcome, Result, Team
from matchpredictor.predictors.predictor import Predictor


class LinearRegressionPredictor(Predictor):
    team_encoding: OneHotEncoder
    model: LogisticRegression

    def __init__(self, model: LogisticRegression, team_encoding: OneHotEncoder):
        self.model = model
        self.team_encoding = team_encoding

    def predict(self, fixture: Fixture) -> Outcome:
        encoded_home_name = self.__encode_team(fixture.home_team)
        encoded_away_name = self.__encode_team(fixture.away_team)

        if encoded_home_name is None:
            return Outcome.AWAY
        if encoded_away_name is None:
            return Outcome.HOME

        X = np.concatenate([encoded_home_name, encoded_away_name], 1)
        pred = self.model.predict(X)

        if pred > 0:
            return Outcome.HOME
        elif pred < 0:
            return Outcome.AWAY
        else:
            return Outcome.DRAW

    def __encode_team(self, team: Team):
        try:
            return self.team_encoding.transform(np.array(team.name).reshape(-1, 1))
        except ValueError:
            return None


def build_model(results: List[Result]) -> Tuple[LogisticRegression, OneHotEncoder]:
    home_names = np.array([r.fixture.home_team.name for r in results])
    away_names = np.array([r.fixture.away_team.name for r in results])
    home_goals = np.array([r.home_goals for r in results])
    away_goals = np.array([r.away_goals for r in results])

    team_names = np.array(list(home_names) + list(away_names)).reshape(-1, 1)
    team_encoding = OneHotEncoder(sparse=False).fit(team_names)

    encoded_home_names = team_encoding.transform(home_names.reshape(-1, 1))
    encoded_away_names = team_encoding.transform(away_names.reshape(-1, 1))

    X = np.concatenate([encoded_home_names, encoded_away_names], 1)
    y = np.sign(home_goals - away_goals)

    model = LogisticRegression(penalty="l2", fit_intercept=False, multi_class="ovr", C=1)
    model.fit(X, y)

    return model, team_encoding


def train_regression_predictor(results: List[Result]) -> LinearRegressionPredictor:
    model, team_encoding = build_model(results)

    return LinearRegressionPredictor(model, team_encoding)
