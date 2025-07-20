from enum import Enum


class DatapointField(str, Enum):
    CONTEXT_TOKEN = "context_token"
    COST = "cost"
    ERROR_CODE = "error_code"
    ERROR_MESSAGE = "error_message"
    ERROR_TYPE = "error_type"
    FEEDBACK = "feedback"
    ID = "id"
    INPUT = "input"
    INPUT_DATETIME = "input_datetime"
    INPUT_TOKENS = "input_tokens"
    INPUT_TOOLS = "input_tools"
    ISSUE_TYPE = "issue_type"
    LATENCY = "latency"
    MODEL_METADATA = "model_metadata"
    OUTPUT_TOKENS = "output_tokens"
    PROVIDER = "provider"
    REQUEST_MODEL_NAME = "request_model_name"
    RESPONSE_MODEL_NAME = "response_model_name"
    RESULT = "result"
    RESULT_DATETIME = "result_datetime"
    RESULT_TOOL_CALLS = "result_tool_calls"
    SOURCE = "source"
    TAGS = "tags"
    TEMPERATURE = "temperature"
    TEST_DATA_POINT_ID = "test_data_point_id"
    TEST_RUN_ID = "test_run_id"
    TIME_CREATED = "time_created"
    USER_METADATA = "user_metadata"

    def __str__(self) -> str:
        return str(self.value)
