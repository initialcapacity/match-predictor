import csv
from typing import List, Dict

from matchpredictor.results.result import Result, Fixture, Team, Outcome


def load_results(file: str = 'england-training.csv') -> List[Result]:
    with open(file) as csvfile:
        rows = csv.DictReader(csvfile)

        return list(map(row_to_result, rows))


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
