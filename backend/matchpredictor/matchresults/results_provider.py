import csv
import pathlib
from os import path
from typing import Dict, Callable, List, Optional, cast

from matchpredictor.matchresults.result import Result, Fixture, Team, Outcome


def training_results(
        file_name: str,
        year: int,
        result_filter: Callable[[Result], bool] = lambda result: True,
) -> List[Result]:
    return load_results(file_name, lambda r: result_filter(r) and r.season < year)


def validation_results(
        file_name: str,
        year: int,
        result_filter: Callable[[Result], bool] = lambda result: True
) -> List[Result]:
    return load_results(file_name, lambda r: result_filter(r) and r.season == year)


def load_results(
        file_name: str,
        result_filter: Callable[[Result], bool] = lambda result: True,
) -> List[Result]:
    backend_folder = pathlib.Path(__file__).parent.parent.parent
    file_path = path.join(backend_folder, 'data', f'{file_name}.csv')

    def match_outcome(home_goals: int, away_goals: int) -> Outcome:
        if home_goals > away_goals:
            return Outcome.HOME
        if away_goals > home_goals:
            return Outcome.AWAY
        return Outcome.DRAW

    def result_from_row(row: Dict[str, str]) -> Optional[Result]:
        try:
            home_goals = int(row['score1'])
            away_goals = int(row['score2'])

            return Result(
                fixture=Fixture(
                    home_team=Team(row['team1']),
                    away_team=Team(row['team2']),
                    league=row['league']
                ),
                outcome=match_outcome(home_goals, away_goals),
                home_goals=home_goals,
                away_goals=away_goals,
                season=int(row['season'])
            )
        except ValueError:
            return None

    with open(file_path) as training_data:
        rows = csv.DictReader(training_data)
        results = filter(lambda r: type(r) is Result and result_filter(r), map(result_from_row, rows))

        return cast(List[Result], list(results))
