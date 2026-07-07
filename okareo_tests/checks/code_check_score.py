from okareo.checks import CheckResponse, CodeBasedCheck


class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(model_output: str, scenario_input: str, scenario_result: str, metadata: dict, model_input: str) -> CheckResponse:  # fmt: skip
        return CheckResponse(
            score=len(model_output),
            explanation="Length of the model output.",
        )
