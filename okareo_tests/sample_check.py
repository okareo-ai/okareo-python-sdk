from okareo.checks import CodeBasedCheck


class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(model_output: str, scenario_input: str, scenario_result: str, metadata: dict) -> bool:  # fmt: skip
        return (
            True
            if len(model_output + scenario_input + scenario_result) >= 20
            else False
        )
