from matchpredictor.evaluation.reporter import LabeledPredictor, Reporter
from matchpredictor.matchresults.results_provider import load_results
from matchpredictor.predictors.home_predictor import HomePredictor
from matchpredictor.predictors.past_results_predictor import train_results_predictor
from matchpredictor.predictors.scoring_rate_predictor import train_scoring_predictor

england_training_data = load_results('england-training.csv', result_filter=lambda result: result.fixture.season >= 2017)
england_validation_data = load_results('england-validation.csv')
simulations = 300

england_reporter = Reporter(
    "England 2019",
    england_validation_data,
    [LabeledPredictor("home", HomePredictor()),
     LabeledPredictor("results", train_results_predictor(england_training_data)),
     LabeledPredictor("scoring", train_scoring_predictor(england_training_data, 300)), ]
)

italy_training_data = load_results('italy-training.csv', result_filter=lambda result: result.fixture.season >= 2017)
italy_validation_data = load_results('italy-validation.csv')

italy_reporter = Reporter(
    "Italy 2019",
    italy_validation_data,
    [LabeledPredictor("home", HomePredictor()),
     LabeledPredictor("results", train_results_predictor(italy_training_data)),
     LabeledPredictor("scoring", train_scoring_predictor(italy_training_data, 300)), ]
)

print()
england_reporter.run_report()
italy_reporter.run_report()
