from dataclasses import dataclass
from typing import Iterable, List

from matchpredictor.evaluation.evaluator import Evaluator
from matchpredictor.matchresults.result import Result
from matchpredictor.model.model_provider import Model, ModelProvider


@dataclass
class PredictionReport(object):
    label: str
    accuracy: float
    time_elapsed: float


class Reporter:
    def __init__(self, title: str, validation_data: Iterable[Result], model_provider: ModelProvider) -> None:
        self.title = title
        self.validation_data = validation_data
        self.model_provider = model_provider
        self.reports: List[PredictionReport] = []

    def run_report(self) -> None:
        reports = map(self.__calculate_accuracy, self.model_provider.list())
        self.__print_reports(reports)

    def __print_reports(self, reports: Iterable[PredictionReport]) -> None:
        print()
        print("=" * (len(self.title) + 2))
        print(f" {self.title} ")
        print("=" * (len(self.title) + 2))
        print()

        print(" {:<30} | {:<8} | {:<10}".format("Predictor", "Accuracy", "Elapsed"))
        print("-" * 32 + "+" + "-" * 10 + "+" + "-" * 11)

        format_line = " {:<30} | {:<8.6f} | {:<8.6f}s"
        for r in reports:
            print(format_line.format(r.label, r.accuracy, r.time_elapsed))

        print()

    def __calculate_accuracy(self, model: Model) -> PredictionReport:
        accuracy, time_elapsed = Evaluator(model.predictor).measure_accuracy(self.validation_data)

        return PredictionReport(
            label=model.name,
            accuracy=accuracy,
            time_elapsed=time_elapsed
        )
