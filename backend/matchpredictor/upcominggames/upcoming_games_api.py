from dataclasses import dataclass
from datetime import datetime
from typing import List

from flask import Blueprint, Response, jsonify

from matchpredictor.upcominggames.football_data_api_client import FootballDataApiClient, FootballDataMatchesResponse, \
    MatchJson


@dataclass(frozen=True)
class UpcomingGame:
    league: str
    home: str
    away: str


@dataclass(frozen=True)
class UpcomingGamesResponse:
    games: List[UpcomingGame]


@dataclass(frozen=True)
class LeagueMappingKey:
    areaName: str
    competitionName: str

    def default_value(self) -> str:
        return f'{self.areaName} {self.competitionName}'


league_mapping = {
    LeagueMappingKey(areaName='Netherlands', competitionName='Eredivisie'): 'Dutch Eredivisie',
    LeagueMappingKey(areaName='England', competitionName='Championship'): 'English League Championship',
}


def response_from_football_data_matches(matches_response: FootballDataMatchesResponse) -> UpcomingGamesResponse:
    def build_upcoming_game(match_json: MatchJson) -> UpcomingGame:
        league_mapping_key = LeagueMappingKey(
            areaName=match_json.area.name,
            competitionName=match_json.competition.name
        )

        return UpcomingGame(
            league=league_mapping.get(league_mapping_key, league_mapping_key.default_value()),
            home=match_json.homeTeam.shortName,
            away=match_json.awayTeam.shortName,
        )

    games = [
        build_upcoming_game(m) for m in matches_response.matches
    ]

    return UpcomingGamesResponse(games)


def upcoming_games_api(api_client: FootballDataApiClient) -> Blueprint:
    api = Blueprint('upcoming_games_api', __name__)

    @api.get('/upcoming-games/<date_from_str>')
    def list_upcoming_games(date_from_str: str) -> Response:
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(f'Invalid date format: {date_from_str}', 400)

        maybe_football_data_api_matches = api_client.fetch_matches(date_from)

        if maybe_football_data_api_matches is None:
            return Response('Oops', 503)

        matches = maybe_football_data_api_matches
        upcoming_games_response = response_from_football_data_matches(matches)

        return jsonify(upcoming_games_response)

    return api
