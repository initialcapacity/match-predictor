import csv
import pathlib
from io import StringIO
from os import path
from typing import Dict, Callable, List, Optional, cast

import requests

from matchpredictor.matchresults.result import Result, Fixture, Team, Outcome


def download_csv(file_name: str) -> str:
    response = requests.request(
        method='GET',
        url=f'https://projects.fivethirtyeight.com/soccer-api/club/{file_name}.csv'
    )
    if response.status_code != 200:
        raise Exception(f'Expected response status code of 200, got {response.status_code} instead')

    return response.content.decode('utf-8')


def load_csv_from_disk(file_name: str) -> str:
    backend_folder = pathlib.Path(__file__).parent.parent.parent
    file_path = path.join(backend_folder, 'data', f'{file_name}.csv')

    with open(file_path) as training_data:
        return training_data


def training_results(
        file_name: str,
        year: int,
        result_filter: Callable[[Result], bool] = lambda result: True,
        get_csv: Callable[[str], str] = download_csv,
) -> List[Result]:
    return load_results(file_name, lambda r: result_filter(r) and r.season < year, get_csv)


def validation_results(
        file_name: str,
        year: int,
        result_filter: Callable[[Result], bool] = lambda result: True
) -> List[Result]:
    return load_results(file_name, lambda r: result_filter(r) and r.season == year)


def load_results(
        file_name: str,
        result_filter: Callable[[Result], bool] = lambda result: True,
        get_csv: Callable[[str], str] = download_csv,
) -> List[Result]:

    def game_outcome(away_goals: int, home_goals: int) -> Outcome:
        outcome = Outcome.DRAW

        if away_goals > home_goals:
            outcome = Outcome.AWAY
        if home_goals > away_goals:
            outcome = Outcome.HOME

        return outcome

    def result_from_row(row: Dict[str, str]) -> Optional[Result]:
        try:
            away_goals = int(row['score2'])
            home_goals = int(row['score1'])

            return Result(
                fixture=Fixture(
                    home_team=Team(row['team1']),
                    away_team=Team(row['team2']),
                    league=row['league']
                ),
                outcome=game_outcome(away_goals, home_goals),
                home_goals=home_goals,
                away_goals=away_goals,
                season=int(row['season']),
            )
        except (TypeError, AttributeError, ValueError):
            return None

    def apply_filter(maybe_result: Optional[Result]) -> bool:
        if maybe_result is None:
            return False

        return result_filter(maybe_result)

    csv_file_content = get_csv(file_name)
    rows = csv.DictReader(StringIO(csv_file_content))
    results = map(result_from_row, rows)
    results_filter = filter(apply_filter, results)

    return cast(List[Result], list(results_filter))
