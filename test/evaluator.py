from fractions import Fraction
from typing import List

from matchpredictor.results.result import Result
from matchpredictor.results.results_provider import load_results
from matchpredictor.predictors.predictor import Predictor


class Evaluator(object):
    def __init__(self, predictor: Predictor) -> None:
        self.predictor = predictor

    def proportion_correct(self, results: List[Result]) -> Fraction:
        correct_predictions = sum([self.__is_correct(m) for m in results])

        return Fraction(correct_predictions, len(results))

    def __is_correct(self, result: Result) -> bool:
        return self.predictor.predict(result.fixture) == result.outcome


def measure_accuracy(predictor: Predictor):
    results = load_results(file='england-validation.csv')
    evaluator = Evaluator(predictor)

    return evaluator.proportion_correct(results)
