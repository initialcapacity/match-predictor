from dataclasses import dataclass
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

    def fetch_matches(self) -> Optional[FootballDataMatchesResponse]:
        try:
            football_data_api_response = requests \
                .get('https://api.football-data.org/v4/matches', headers={'X-Auth-Token': self.api_key}) \
                .json()

            return dacite.core.from_dict(
                data_class=FootballDataMatchesResponse,
                data=football_data_api_response
            )

        except requests.JSONDecodeError:
            return None
        except dacite.DaciteError:
            return None
