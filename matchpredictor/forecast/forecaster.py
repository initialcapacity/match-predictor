from typing import Optional

from matchpredictor.matchresults.result import Fixture, Team, Outcome
from matchpredictor.predictors.predictor import Predictor, PredictorProvider


class Forecaster:
    def __init__(self, provider: PredictorProvider) -> None:
        self.provider = provider

    def forecast(self, league: str, home_team_name: str, away_team_name: str, season: int) -> Optional[Outcome]:
        predictor = self.provider.get(league)
        if predictor is None:
            return None

        fixture = Fixture(
            home_team=Team(home_team_name),
            away_team=Team(away_team_name),
            season=season,
        )

        return predictor.predict(fixture)
