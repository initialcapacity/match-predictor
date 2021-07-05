from dataclasses import dataclass
from typing import Iterable

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


class Reporter:
    def __init__(self, title: str, validation_data: Iterable[Result], predictors: Iterable[LabeledPredictor]) -> None:
        self.title = title
        self.validation_data = validation_data
        self.predictors = predictors
        self.reports = []

    def run_report(self):
        reports = map(self.__calculate_accuracy, self.predictors)
        self.__print_reports(reports)

    def __print_reports(self, reports: Iterable[PredictionReport]):
        print("=" * len(self.title))
        print(self.title)
        print("=" * len(self.title))
        print()

        print("{:<20} |  {:<8}".format("Predictor", "Accuracy"))
        print("-" * 21 + "+" + "-" * 10)

        format_line = "{:<20} |  {:<8.6f}"
        for r in reports:
            print(format_line.format(r.label, r.accuracy))

        print()

    def __calculate_accuracy(self, predictor: LabeledPredictor) -> PredictionReport:
        accuracy = Evaluator(predictor.predictor).measure_accuracy(self.validation_data)

        return PredictionReport(
            label=predictor.label,
            accuracy=float(accuracy),
        )
