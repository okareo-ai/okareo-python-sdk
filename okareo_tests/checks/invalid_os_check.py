import os  # noqa: F401 - intentionally unused, testing validation

from okareo.checks import CodeBasedCheck


class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(
        model_output: str,
        scenario_input: str,
        scenario_result: str,
        metadata: dict,
        model_input: str,
    ) -> bool:
        # This check uses os module which is not allowed
        return True
