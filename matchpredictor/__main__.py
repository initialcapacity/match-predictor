from matchpredictor.evaluation.reporter import LabeledPredictor, Reporter
from matchpredictor.matchresults.results_provider import load_results
from matchpredictor.predictors.home_predictor import HomePredictor
from matchpredictor.predictors.past_results_predictor import calculate_table, PastResultsPredictor
from matchpredictor.predictors.scoring_rate_predictor import ScoringRatePredictor, calculate_scoring_rates

training_data = load_results(data_file='england-training.csv',
                             result_filter=lambda result: result.fixture.season >= 2017)
validation_data = load_results(data_file='england-validation.csv')

home_predictor = HomePredictor()
past_predictor = PastResultsPredictor(calculate_table(training_data))
scoring_predictor = ScoringRatePredictor(calculate_scoring_rates(training_data))

reporter = Reporter(
    "England 2019",
    validation_data,
    [
        LabeledPredictor("home", home_predictor),
        LabeledPredictor("past", past_predictor),
        LabeledPredictor("scoring", scoring_predictor),
    ]
)

print()
reporter.run_report()
