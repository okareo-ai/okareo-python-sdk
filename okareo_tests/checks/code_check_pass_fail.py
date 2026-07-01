from okareo.checks import CheckOutputType, CheckResponse, CodeBasedCheck


class Check(CodeBasedCheck):
    check_type = CheckOutputType.PASS_FAIL

    @staticmethod
    def evaluate(model_output: str, scenario_input: str, scenario_result: str, metadata: dict, model_input: str) -> CheckResponse:  # fmt: skip
        passed = len(model_output) > 0
        return CheckResponse(
            score=passed,
            explanation="Non-empty output." if passed else "Empty output.",
        )
