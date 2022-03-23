from typing import Iterable, Dict

from matchpredictor.matchresults.result import Outcome, Fixture, Result, Team
from matchpredictor.predictors.predictor import Predictor, Prediction


class PointsTable:
    def __init__(self) -> None:
        self.points_dict: Dict[str, int] = {}

    def points_for(self, team: Team) -> int:
        return self.points_dict.get(team.name, 0)

    def record_win(self, team: Team) -> None:
        self.__add_points(team, 3)

    def record_draw(self, team: Team) -> None:
        self.__add_points(team, 1)

    def __add_points(self, team: Team, points: int) -> None:
        previous_points = self.points_dict.get(team.name, 0)
        self.points_dict[team.name] = previous_points + points


def past_results_predictor(table: PointsTable) -> Predictor:

    def predict(fixture: Fixture) -> Prediction:
        home_points = table.points_for(fixture.home_team)
        away_points = table.points_for(fixture.away_team)

        if home_points > away_points:
            return Prediction(Outcome.HOME)
        elif home_points < away_points:
            return Prediction(Outcome.AWAY)
        else:
            return Prediction(Outcome.DRAW)

    return predict


def calculate_table(results: Iterable[Result]) -> PointsTable:
    table = PointsTable()

    for result in results:
        if result.outcome == Outcome.HOME:
            table.record_win(result.fixture.home_team)
        elif result.outcome == Outcome.AWAY:
            table.record_win(result.fixture.away_team)
        else:
            table.record_draw(result.fixture.home_team)
            table.record_draw(result.fixture.away_team)

    return table


def train_results_predictor(results: Iterable[Result]) -> Predictor:
    return past_results_predictor(calculate_table(results))
