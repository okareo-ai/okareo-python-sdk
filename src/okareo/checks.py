import inspect
from abc import ABC, abstractmethod
from enum import Enum
from typing import Union


class BaseCheck(ABC):
    """
    Base class for defining checks
    """

    @staticmethod
    @abstractmethod
    def evaluate(
        model_output: str, scenario_input: str, scenario_result: str, metadata: dict
    ) -> Union[bool, int, float]:
        """
        Evaluate your model output, scenario input, scenario result, and metadata
        to determine if the data should pass or fail the check.
        """

    def check_config(self) -> dict:
        """
        Returns a dictionary of configuration parameters that will be passed to the API.
        """
        return {}


class CheckOutputType(Enum):
    """
    Enum for the type of output that the check will produce. This is used in ModelBasedCheck.
    """

    SCORE = "score"
    PASS_FAIL = "pass_fail"


class ModelBasedCheck(BaseCheck):
    """
    Check that uses a prompt template to evaluate the data.

    The prompt template should be a string that includes at least one of
    the following placeholders, which will be replaced with the actual values:
    - "{model_output}" -> corresponds to the model's output
    - "{scenario_input}" -> corresponds to the scenario input
    - "{scenario_result}" -> corresponds to the scenario result

    Example of how a template could be used: "Count the words in the following: {model_output}"

    The check output type should be one of the following:
    - CheckOutputType.SCORE -> this template should ask prompt the model a score (single number)
    - CheckOutputType.PASS_FAIL -> this template should prompt the model for a boolean value (True/False)
    """

    def __init__(self, prompt_template: str, check_type: CheckOutputType):
        """Initialize the check with a prompt template and check type"""
        self.prompt_template = prompt_template
        self.check_type = check_type.value

    def check_config(self) -> dict:
        return {"prompt_template": self.prompt_template, "type": self.check_type}

    @staticmethod
    def evaluate(
        model_output: str,
        scenario_input: str,
        scenario_result: str,
        metadata: dict,
    ) -> Union[bool, int, float]:
        raise NotImplementedError("Evaluate method is handled on server.")


class CodeBasedCheck(BaseCheck):
    """
    A check that uses code to evaluate the data

    To use this check:
    1. Create a new Python file (not in a notebook).
    2. In this file, define a class named 'Check' that inherits from CodeBasedCheck.
    3. Implement the `evaluate` method in your Check class.
    4. Include any additional code used by your check in the same file.

    Example:
    ```
    # In my_custom_check.py
    from okareo.checks import CodeBasedCheck

    class Check(CodeBasedCheck):
        @staticmethod
        @abstractmethod
        def evaluate(
            model_output: str, scenario_input: str, scenario_result: str, metadata: dict
        ) -> Union[bool, int, float]:
            # Your code here
            pass
    ```
    """

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
