import time
from typing import Iterable, Tuple

from matchpredictor.matchresults.result import Result
from matchpredictor.predictors.predictor import Predictor


class Evaluator(object):
    def __init__(self, predictor: Predictor) -> None:
        self.predictor = predictor

    def measure_accuracy(self, validation_data: Iterable[Result]) -> Tuple[float, float]:
        results = list(validation_data)

        start_time = time.time()
        correct_predictions = sum([self.__is_correct(m) for m in results])
        time_elapsed = time.time() - start_time

        return correct_predictions / len(results), time_elapsed

    def __is_correct(self, result: Result) -> bool:
        prediction = self.predictor.predict(result.fixture)
        return prediction.outcome == result.outcome
