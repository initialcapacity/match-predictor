from dataclasses import dataclass
from typing import Dict, Optional, List

from matchpredictor.predictors.predictor import Predictor, InProgressPredictor


@dataclass(frozen=True)
class Model(object):
    name: str
    predictor: Predictor | InProgressPredictor

    def predicts_in_progress(self) -> bool:
        return isinstance(self.predictor, InProgressPredictor)


class ModelProvider(object):
    def __init__(self, models: List[Model]) -> None:
        self.__models: Dict[str, Model] = {}
        for model in models:
            self.__models[model.name] = model

    def get_predictor(self, model_name: str) -> Optional[Predictor]:
        model = self.__models.get(model_name)

        if model is None:
            return None

        return model.predictor

    def get_in_progress_predictor(self, model_name: str) -> Optional[InProgressPredictor]:
        model = self.__models.get(model_name)

        if model is None or not isinstance(model.predictor, InProgressPredictor):
            return None

        return model.predictor

    def list(self) -> List[Model]:
        return list(self.__models.values())
