from dataclasses import dataclass
from datetime import date
import datetime
from typing import Optional

import dacite
import requests


@dataclass(frozen=True)
class NamedJson:
    name: str


@dataclass(frozen=True)
class TeamJson:
    shortName: str


@dataclass(frozen=True)
class MatchJson:
    area: NamedJson
    competition: NamedJson
    homeTeam: TeamJson
    awayTeam: TeamJson


@dataclass(frozen=True)
class FootballDataMatchesResponse:
    matches: list[MatchJson]


class FootballDataApiClient:

    def __init__(self, api_key: str):
        self.api_key = api_key

    nine_days = datetime.timedelta(days=9)

    def fetch_matches(self, date_from: date) -> Optional[FootballDataMatchesResponse]:
        date_to = date_from + self.nine_days

        try:
            football_data_api_response = requests \
                .get(f'https://api.football-data.org/v4/matches?dateFrom={date_from}&dateTo={date_to}', headers={'X-Auth-Token': self.api_key}) \
                .json()

            return dacite.core.from_dict(
                data_class=FootballDataMatchesResponse,
                data=football_data_api_response
            )

        except requests.JSONDecodeError:
            return None
        except dacite.DaciteError:
            return None
