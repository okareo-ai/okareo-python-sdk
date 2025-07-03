from okareo.checks import CodeBasedCheck

class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(scenario_input: str) -> int:  # fmt: skip
        return len(scenario_input)