from okareo.checks import CodeBasedCheck


class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(model_output: str, scenario_input: str, scenario_result: str, metadata: dict, model_input: str) -> bool:  # fmt: skip
        # Check if metadata is empty
        if metadata.get("tool_calls"):
            return True if len(metadata["tool_calls"]) > 0 else False
        return False
