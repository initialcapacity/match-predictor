from dataclasses import dataclass
from typing import List

from flask import Blueprint, Response, jsonify

from matchpredictor.upcominggames.football_data_api_client import FootballDataApiClient, FootballDataMatchesResponse, \
    MatchJson


@dataclass(frozen=True)
class Team:
    name: str
    leagues: List[str]


@dataclass(frozen=True)
class UpcomingGame:
    home: Team
    away: Team


@dataclass(frozen=True)
class UpcomingGamesResponse:
    games: List[UpcomingGame]


def response_from_football_data_matches(matches_response: FootballDataMatchesResponse) -> UpcomingGamesResponse:
    def build_upcoming_game(match_json: MatchJson) -> UpcomingGame:
        return UpcomingGame(
            home=Team(name=match_json.homeTeam.name, leagues=[match_json.competition.name]),
            away=Team(name=match_json.awayTeam.name, leagues=[match_json.competition.name]),
        )

    games = [
        build_upcoming_game(m) for m in matches_response.matches
    ]

    return UpcomingGamesResponse(games)


def upcoming_games_api(api_client: FootballDataApiClient) -> Blueprint:
    api = Blueprint("upcoming_games_api", __name__)

    @api.route('/upcoming-games', methods=["GET"])
    def list_upcoming_games() -> Response:
        maybe_football_data_api_matches = api_client.fetch_matches()

        if maybe_football_data_api_matches is None:
            return Response("Oops", 503)

        matches = maybe_football_data_api_matches
        upcoming_games_response = response_from_football_data_matches(matches)

        return jsonify(upcoming_games_response)

    return api
