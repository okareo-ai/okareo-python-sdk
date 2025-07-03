from okareo.checks import CodeBasedCheck


class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(model_output: str, scenario_input: str, scenario_result: str, metadata: dict, model_input: str) -> int:  # fmt: skip
        model_input_len = sum([len(str(mi)) for mi in model_input])
        return model_input_len > len(scenario_input)
