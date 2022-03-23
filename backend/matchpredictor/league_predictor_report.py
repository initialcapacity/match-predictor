from matchpredictor.evaluation.reporter import Reporter, LabeledPredictor
from matchpredictor.matchresults.result import Result
from matchpredictor.matchresults.results_provider import training_results, validation_results
from matchpredictor.predictors.home_predictor import home_predictor
from matchpredictor.predictors.linear_regression_predictor import train_regression_predictor
from matchpredictor.predictors.past_results_predictor import train_results_predictor
from matchpredictor.predictors.simulation_predictor import train_offense_predictor, \
    train_offense_and_defense_predictor


def predictor_report_for(league: str, year: int) -> None:
    def matches_league(result: Result) -> bool:
        return result.fixture.league == league

    training_data = training_results("spi_matches", year,
                                     lambda result: result.season >= year - 3 and matches_league(result))
    validation_data = validation_results("spi_matches", year, matches_league)

    Reporter(
        f"{league} {year}",
        validation_data,
        [LabeledPredictor("home", home_predictor),
         LabeledPredictor("points", train_results_predictor(training_data)),
         LabeledPredictor("scoring coarse", train_offense_predictor(training_data, 30)),
         LabeledPredictor("scoring", train_offense_predictor(training_data, 300)),
         LabeledPredictor("enhanced scoring", train_offense_and_defense_predictor(training_data, 300)),
         LabeledPredictor("linear regression", train_regression_predictor(training_data)), ]
    ).run_report()
