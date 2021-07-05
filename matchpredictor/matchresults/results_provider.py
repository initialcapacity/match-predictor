import csv
from os import path
from typing import Dict, Callable, List

from matchpredictor.matchresults.result import Result, Fixture, Team, Outcome


def load_results(data_file: str, result_filter: Callable[[Result], bool] = lambda result: True) -> List[Result]:
    with open(path.join('data', data_file)) as training_data:
        rows = csv.DictReader(training_data)

        return list(filter(result_filter, map(row_to_result, rows)))


def row_to_result(row: Dict[str, str]) -> Result:
    fixture = Fixture(
        home_team=Team(row['home']),
        away_team=Team(row['visitor']),
        tier=int(row['tier']),
        season=int(row['Season']),
    )

    outcome = {
        "H": Outcome.HOME,
        "A": Outcome.AWAY,
        "D": Outcome.DRAW,
    }[row['result']]

    return Result(
        fixture=fixture,
        outcome=outcome,
        home_goals=int(row['hgoal']),
        away_goals=int(row['vgoal']),
    )
