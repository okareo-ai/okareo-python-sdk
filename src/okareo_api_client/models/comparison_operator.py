from enum import Enum


class ComparisonOperator(str, Enum):
    CONTAINS = "contains"
    EQUAL = "equal"
    GREATER_THAN = "greater_than"
    GREATER_THAN_OR_EQUAL = "greater_than_or_equal"
    IS_SET = "is_set"
    LESS_THAN = "less_than"
    LESS_THAN_OR_EQUAL = "less_than_or_equal"
    NOT_CONTAINS = "not_contains"
    NOT_EQUAL = "not_equal"
    NOT_SET = "not_set"

    def __str__(self) -> str:
        return str(self.value)
