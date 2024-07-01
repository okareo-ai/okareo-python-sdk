from abc import ABC, abstractmethod
from typing import Union


class BaseCheck(ABC):
    @staticmethod
    @abstractmethod
    def evaluate(
        model_output: str, scenario_input: str, scenario_result: str
    ) -> Union[bool, int, float]:
        pass
