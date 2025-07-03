from okareo.checks import CodeBasedCheck


class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(scenario_input: str, model_input: list) -> bool:  # fmt: skip
        model_input_len = sum([len(str(mi)) for mi in model_input])
        return model_input_len > len(scenario_input)
