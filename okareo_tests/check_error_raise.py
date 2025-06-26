from okareo.checks import CodeBasedCheck


class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(model_output: str, scenario_input: str, scenario_result: str, metadata: dict) -> bool:  # fmt: skip
        # Check if metadata is empty
        if scenario_input != "dummyinput":
            raise ValueError("Check errored out.")
        return True
