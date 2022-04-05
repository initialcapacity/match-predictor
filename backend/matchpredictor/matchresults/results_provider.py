import csv
from io import StringIO
from typing import Dict, Callable, List, Optional, cast

import requests

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

    response = requests.request(
        method='GET',
        url=f'https://projects.fivethirtyeight.com/soccer-api/club/{file_name}.csv'
    )

    csv_file_content = response.content.decode('utf-8')

    rows = csv.DictReader(StringIO(csv_file_content))
    maybe_results = map(result_from_row, rows)
    filtered_results = filter(lambda r: type(r) is Result and result_filter(r), maybe_results)

    return cast(List[Result], list(filtered_results))
