from dataclasses import dataclass
from typing import Iterable, List

from matchpredictor.evaluation.evaluator import Evaluator
from matchpredictor.matchresults.result import Result
from matchpredictor.predictors.predictor import Predictor


@dataclass
class LabeledPredictor(object):
    label: str
    predictor: Predictor


@dataclass
class PredictionReport(object):
    label: str
    accuracy: float
    time_elapsed: float


class Reporter:
    def __init__(self, title: str, validation_data: Iterable[Result], predictors: Iterable[LabeledPredictor]) -> None:
        self.title = title
        self.validation_data = validation_data
        self.predictors = predictors
        self.reports: List[PredictionReport] = []

    def run_report(self) -> None:
        reports = map(self.__calculate_accuracy, self.predictors)
        self.__print_reports(reports)

    def __print_reports(self, reports: Iterable[PredictionReport]) -> None:
        print()
        print("=" * (len(self.title) + 2))
        print(f" {self.title} ")
        print("=" * (len(self.title) + 2))
        print()

        print(" {:<20} | {:<8} | {:<10}".format("Predictor", "Accuracy", "Elapsed"))
        print("-" * 22 + "+" + "-" * 10 + "+" + "-" * 11)

        format_line = " {:<20} | {:<8.6f} | {:<8.6f}s"
        for r in reports:
            print(format_line.format(r.label, r.accuracy, r.time_elapsed))

        print()

    def __calculate_accuracy(self, predictor: LabeledPredictor) -> PredictionReport:
        accuracy, time_elapsed = Evaluator(predictor.predictor).measure_accuracy(self.validation_data)

        return PredictionReport(
            label=predictor.label,
            accuracy=accuracy,
            time_elapsed=time_elapsed
        )
