from okareo.checks import CodeBasedCheck

class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(model_input: list) -> int:  # fmt: skip
        return len(model_input)