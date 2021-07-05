from os import path
from fractions import Fraction
from typing import List, Iterable

from matchpredictor.matchresults.result import Result
from matchpredictor.matchresults.results_provider import load_results
from matchpredictor.predictors.predictor import Predictor


class Evaluator(object):
    def __init__(self, predictor: Predictor) -> None:
        self.predictor = predictor

    def measure_accuracy(self, validation_data: Iterable[Result]):
        return self.__proportion_correct(list(validation_data))

    def __proportion_correct(self, results: List[Result]) -> Fraction:
        correct_predictions = sum([self.__is_correct(m) for m in results])

        return Fraction(correct_predictions, len(results))

    def __is_correct(self, result: Result) -> bool:
        return self.predictor.predict(result.fixture) == result.outcome
