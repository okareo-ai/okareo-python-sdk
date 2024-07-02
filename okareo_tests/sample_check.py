from okareo.checks import CodeBasedCheck


class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(model_output: str, scenario_input: str, scenario_result: str) -> bool:
        return (
            True
            if len(model_output + scenario_input + scenario_result) >= 20
            else False
        )
