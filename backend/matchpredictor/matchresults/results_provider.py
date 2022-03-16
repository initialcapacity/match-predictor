import csv
import pathlib
from os import path
from typing import Dict, Callable, List, Optional, cast

from matchpredictor.matchresults.result import Result, Fixture, Team, Outcome


def load_five_thirty_eight_spi_results(
        file_name: str,
        max_year: int,
) -> List[Result]:
    backend_folder = pathlib.Path(__file__).parent.parent.parent
    file_path = path.join(backend_folder, 'data', f'{file_name}.csv')

    def is_season_in_range(row: Dict[str, str]) -> bool:
        return int(row['season']) < max_year

    def game_outcome(home_goals: int, away_goals: int) -> Outcome:
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
                outcome=game_outcome(home_goals, away_goals),
                home_goals=home_goals,
                away_goals=away_goals,
                season=int(row['season'])
            )
        except ValueError:
            return None

    def is_result(maybe_result: Optional[Result]) -> bool:
        return type(maybe_result) is Result

    with open(file_path) as training_data:
        rows = csv.DictReader(training_data)
        results = filter(is_result, map(result_from_row, filter(is_season_in_range, rows)))

        return cast(List[Result], list(results))


def training_results(
        country: str,
        year: int,
        result_filter: Callable[[Result], bool] = lambda result: True,
) -> List[Result]:
    return __load_results(f"{country}.csv", country, lambda r: result_filter(r) and r.season < year)


def validation_results(
        country: str,
        year: int,
        result_filter: Callable[[Result], bool] = lambda result: True
) -> List[Result]:
    return __load_results(f"{country}.csv", country, lambda r: result_filter(r) and r.season == year)


def __load_results(data_file: str, country: str, result_filter: Callable[[Result], bool]) -> List[Result]:
    with open(path.join('data', data_file)) as training_data:
        rows = csv.DictReader(training_data)

        return list(filter(result_filter, map(lambda row: __row_to_result(row, country), rows)))


def __row_to_result(row: Dict[str, str], country: str) -> Result:
    fixture = Fixture(
        home_team=Team(row['home']),
        away_team=Team(row['visitor']),
        league=f"{country} {row['tier']}"
    )

    home_goals = int(row['hgoal'])
    away_goals = int(row['vgoal'])
    outcome = __determine_outcome(away_goals, home_goals)

    return Result(
        fixture=fixture,
        outcome=outcome,
        home_goals=home_goals,
        away_goals=away_goals,
        season=int(row['Season']),
    )


def __determine_outcome(away_goals: int, home_goals: int) -> Outcome:
    if home_goals > away_goals:
        return Outcome.HOME
    elif home_goals < away_goals:
        return Outcome.AWAY
    else:
        return Outcome.DRAW
