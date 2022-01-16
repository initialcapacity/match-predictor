from typing import Iterable

from matchpredictor.predictors.predictor import Predictor
from matchpredictor.matchresults.result import Outcome, Fixture, Result, Team


class PointsTable:
    def __init__(self):
        self.points_dict = {}

    def points_for(self, team: Team) -> int:
        return self.points_dict.get(team.name, 0)

    def record_win(self, team: Team):
        self.__add_points(team, 3)

    def record_draw(self, team: Team):
        self.__add_points(team, 1)

    def __add_points(self, team: Team, points: int):
        previous_points = self.points_dict.get(team.name, 0)
        self.points_dict[team.name] = previous_points + points


class PastResultsPredictor(Predictor):
    def __init__(self, table: PointsTable):
        self.table = table

    def predict(self, fixture: Fixture) -> Outcome:
        home_points = self.table.points_for(fixture.home_team)
        away_points = self.table.points_for(fixture.away_team)

        if home_points > away_points:
            return Outcome.HOME
        elif home_points < away_points:
            return Outcome.AWAY
        else:
            return Outcome.DRAW


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


def train_results_predictor(results: Iterable[Result]) -> PastResultsPredictor:
    return PastResultsPredictor(calculate_table(results))
