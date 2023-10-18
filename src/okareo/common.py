import os

DEFAULT_BASE_URL = "https://api.okareo.com"
BASE_URL = os.environ.get("BASE_URL", DEFAULT_BASE_URL)

DEFAULT_HTTPX_TIME_OUT = 30
# being generous to support the longer generations
HTTPX_TIME_OUT = float(os.environ.get("HTTPX_TIME_OUT", DEFAULT_HTTPX_TIME_OUT))


class NotJSONError(Exception):
    def __init__(self) -> None:
        super().__init__("Expected JSON response, received non-JSON.")
