from okareo.checks import BaseCheck


class Check(BaseCheck):
    @staticmethod
    def evaluate(model_output: str, scenario_input: str, scenario_result: str) -> bool:
        return True if len(model_output + scenario_input + scenario_result) >= 20 else False