from matchpredictor.app import build_model_provider
from matchpredictor.evaluation.reporter import Reporter
from matchpredictor.matchresults.result import Result
from matchpredictor.matchresults.results_provider import training_results, validation_results


def predictor_report_for(league: str, year: int) -> None:
    def matches_league(result: Result) -> bool:
        return result.fixture.league == league

    csv_location = 'https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv'
    training_data = training_results(csv_location, year,
                                     lambda result: result.season >= year - 3 and matches_league(result))
    validation_data = validation_results(csv_location, year, matches_league)

    Reporter(f"{league} {year}", validation_data, build_model_provider(training_data)) \
        .run_report()
