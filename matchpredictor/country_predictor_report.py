from matchpredictor.evaluation.reporter import Reporter, LabeledPredictor
from matchpredictor.matchresults.results_provider import training_results, validation_results
from matchpredictor.predictors.home_predictor import HomePredictor
from matchpredictor.predictors.linear_regression_predictor import train_regression_predictor
from matchpredictor.predictors.past_results_predictor import train_results_predictor
from matchpredictor.predictors.scoring_rate_predictor import train_scoring_predictor


def predictor_report_for(country_name: str, year: int):
    training_data = training_results(f'{country_name}.csv', year, lambda result: result.fixture.season >= year - 2)
    validation_data = validation_results(f'{country_name}.csv', year)

    Reporter(
        f"{country_name.capitalize()} {year}",
        validation_data,
        [LabeledPredictor("home", HomePredictor()),
         LabeledPredictor("points", train_results_predictor(training_data)),
         LabeledPredictor("scoring coarse", train_scoring_predictor(training_data, 30)),
         LabeledPredictor("scoring", train_scoring_predictor(training_data, 300)),
         LabeledPredictor("linear regression", train_regression_predictor(training_data)), ]
    ).run_report()
