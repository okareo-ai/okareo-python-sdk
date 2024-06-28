from abc import ABC, abstractmethod


class BaseCheck(ABC):
    @staticmethod
    @abstractmethod
    def evaluate(
        model_output: str, scenario_input: str, scenario_result: str
    ) -> bool | int | float:
        pass
