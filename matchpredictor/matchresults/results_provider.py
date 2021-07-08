import csv
from os import path
from typing import Dict, Callable, List, Iterable

from matchpredictor.matchresults.result import Result, Fixture, Team, Outcome


def training_results(
        data_file: str,
        year: int,
        result_filter: Callable[[Result], bool] = lambda result: True
) -> List[Result]:
    return _load_results(data_file, lambda r: result_filter(r) and r.fixture.season < year)


def validation_results(
        data_file: str,
        year: int,
        result_filter: Callable[[Result], bool] = lambda result: True
) -> List[Result]:
    return _load_results(data_file, lambda r: result_filter(r) and r.fixture.season == year)


def _load_results(data_file: str, result_filter: Callable[[Result], bool]) -> List[Result]:
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

    home_goals = int(row['hgoal'])
    away_goals = int(row['vgoal'])
    outcome = determine_outcome(away_goals, home_goals)

    return Result(
        fixture=fixture,
        outcome=outcome,
        home_goals=home_goals,
        away_goals=away_goals,
    )


def determine_outcome(away_goals, home_goals):
    if home_goals > away_goals:
        return Outcome.HOME
    elif home_goals < away_goals:
        return Outcome.AWAY
    else:
        return Outcome.DRAW
