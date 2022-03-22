from matchpredictor.evaluation.reporter import Reporter, LabeledPredictor
from matchpredictor.matchresults.result import Result
from matchpredictor.matchresults.results_provider import training_results, validation_results
from matchpredictor.predictors.home_predictor import HomePredictor
from matchpredictor.predictors.linear_regression_predictor import train_regression_predictor
from matchpredictor.predictors.enhanced_scoring_predictor import train_enhanced_scoring_predictor
from matchpredictor.predictors.past_results_predictor import train_results_predictor
from matchpredictor.predictors.scoring_rate_predictor import train_scoring_predictor


def predictor_report_for(league: str, year: int) -> None:
    def matches_league(result: Result) -> bool:
        return result.fixture.league == league

    training_data = training_results("spi_matches", year,
                                     lambda result: result.season >= year - 3 and matches_league(result))
    validation_data = validation_results("spi_matches", year, matches_league)

    Reporter(
        f"{league} {year}",
        validation_data,
        [LabeledPredictor("home", HomePredictor()),
         LabeledPredictor("points", train_results_predictor(training_data)),
         LabeledPredictor("scoring coarse", train_scoring_predictor(training_data, 30)),
         LabeledPredictor("scoring", train_scoring_predictor(training_data, 300)),
         LabeledPredictor("enhanced scoring", train_enhanced_scoring_predictor(training_data, 300)),
         LabeledPredictor("linear regression", train_regression_predictor(training_data)), ]
    ).run_report()
