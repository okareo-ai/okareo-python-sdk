from okareo.checks import CodeBasedCheck


class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(model_output: str, scenario_input: str, scenario_result: str, metadata: dict, model_input: str) -> int:  # fmt: skip
        return len(model_output)
