from dataclasses import dataclass
from typing import Optional, TypeAlias, Callable

from matchpredictor.matchresults.result import Fixture, Outcome


@dataclass
class Prediction:
    outcome: Outcome
    confidence: Optional[float] = None


Predictor: TypeAlias = Callable[[Fixture], Prediction]
