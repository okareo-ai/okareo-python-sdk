from enum import Enum


class DatapointField(str, Enum):
    CONTEXT_TOKEN = "context_token"
    COST = "cost"
    ERROR_CODE = "error_code"
    ERROR_MESSAGE = "error_message"
    FEEDBACK = "feedback"
    INPUT = "input"
    INPUT_DATETIME = "input_datetime"
    INPUT_TOKENS = "input_tokens"
    LATENCY = "latency"
    MODEL_METADATA = "model_metadata"
    OUTPUT_TOKENS = "output_tokens"
    PROVIDER = "provider"
    REQUEST_MODEL_NAME = "request_model_name"
    RESPONSE_MODEL_NAME = "response_model_name"
    RESULT = "result"
    RESULT_DATETIME = "result_datetime"
    SOURCE = "source"
    TAGS = "tags"
    TEMPERATURE = "temperature"
    TIME_CREATED = "time_created"

    def __str__(self) -> str:
        return str(self.value)
