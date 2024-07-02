import inspect
from abc import ABC, abstractmethod
from enum import Enum
from typing import Union


class BaseCheck(ABC):
    @staticmethod
    @abstractmethod
    def evaluate(
        model_output: str, scenario_input: str, scenario_result: str
    ) -> Union[bool, int, float]:
        pass

    def check_config(self) -> dict:
        """
        Returns a dictionary of configuration parameters that will be passed to the API.
        """
        return {}


class CheckType(Enum):
    SCORE = "score"
    PASS_FAIL = "pass_fail"


class ModelBasedCheck(BaseCheck):
    def __init__(self, prompt_template: str, check_type: CheckType):
        self.prompt_template = prompt_template
        self.check_type = check_type.value

    def check_config(self) -> dict:
        return {"prompt_template": self.prompt_template, "type": self.check_type}

    @staticmethod
    def evaluate(
        model_output: str, scenario_input: str, scenario_result: str
    ) -> Union[bool, int, float]:
        raise NotImplementedError("Evaluate method is handled on server.")


class CodeBasedCheck(BaseCheck):
    def check_config(self) -> dict:
        module = inspect.getmodule(self)
        if module is None:
            raise ValueError("Unable to find module for check class")
        try:
            source = inspect.getsource(module)
        except OSError as e:
            raise ValueError(
                "Unable to read source code for check class. Please place the check class in a separate file."
            ) from e
        output_type = inspect.signature(self.evaluate).return_annotation.__name__
        return {"code_contents": source, "type": output_type}
