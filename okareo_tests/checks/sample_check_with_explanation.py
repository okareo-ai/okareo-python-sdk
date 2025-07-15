from okareo.checks import CheckResponse, CodeBasedCheck


class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(model_output: str, scenario_input: str, scenario_result: str, metadata: dict, model_input: str) -> CheckResponse:  # fmt: skip
        return (
            CheckResponse(
                score=True, explanation="The combined length is at least 20 characters."
            )
            if len(model_output + scenario_input + scenario_result + str(model_input))
            + len(metadata)
            >= 20
            else CheckResponse(
                score=False,
                explanation="The combined length is less than 20 characters.",
            )
        )
