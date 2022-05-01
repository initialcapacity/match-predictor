from dataclasses import dataclass
from typing import Dict, Optional, List

from matchpredictor.predictors.predictor import Predictor


@dataclass(frozen=True)
class Model(object):
    name: str
    predictor: Predictor


class ModelProvider(object):
    def __init__(self, models: List[Model]) -> None:
        self.__models: Dict[str, Model] = {}
        for model in models:
            self.add(model)

    def add(self, model: Model) -> None:
        self.__models[model.name] = model

    def get(self, model_name: str) -> Optional[Model]:
        return self.__models.get(model_name)

    def list(self) -> List[Model]:
        return list(self.__models.values())
