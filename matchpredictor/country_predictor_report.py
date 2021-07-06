from matchpredictor.evaluation.reporter import Reporter, LabeledPredictor
from matchpredictor.matchresults.results_provider import load_results
from matchpredictor.predictors.home_predictor import HomePredictor
from matchpredictor.predictors.linear_regression_predictor import train_regression_predictor
from matchpredictor.predictors.past_results_predictor import train_results_predictor
from matchpredictor.predictors.scoring_rate_predictor import train_scoring_predictor


def predictor_report_for(country_name: str):
    training_data = load_results(f'{country_name}-training.csv', lambda result: result.fixture.season >= 2017)
    validation_data = load_results(f'{country_name}-validation.csv')

    Reporter(
        f"{country_name.capitalize()} 2019",
        validation_data,
        [LabeledPredictor("home", HomePredictor()),
         LabeledPredictor("points", train_results_predictor(training_data)),
         LabeledPredictor("scoring", train_scoring_predictor(training_data, 300)),
         LabeledPredictor("linear regression", train_regression_predictor(training_data)), ]
    ).run_report()
