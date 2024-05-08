from abc import ABC, abstractmethod
from typing import Any

class BaseCheck(ABC):
    @staticmethod
    @abstractmethod
    def evaluate(model_output: str, scenario_input: str, scenario_result: str) -> Any:
        pass