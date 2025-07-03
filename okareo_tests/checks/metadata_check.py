from okareo.checks import CodeBasedCheck

class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(metadata: dict) -> int:  # fmt: skip
        return len(metadata)