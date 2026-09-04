import os
from typing import Optional

DEFAULT_BASE_URL = "https://api.okareo.com"
BASE_URL = os.environ.get("OKAREO_BASE_URL") or os.environ.get(
    "BASE_URL", DEFAULT_BASE_URL
)

DEFAULT_HTTPX_TIME_OUT = 30
# being generous to support the longer generations
# kept for backwards compatibility; use get_httpx_time_out() to read the setting
HTTPX_TIME_OUT = float(os.environ.get("HTTPX_TIME_OUT", DEFAULT_HTTPX_TIME_OUT))


def get_httpx_time_out() -> Optional[float]:
    """Request timeout in seconds, or None to leave requests untimed.

    HTTPX_TIME_OUT is applied only when it is actually set in the environment.
    Requests have run untimed since the generated client was introduced, and
    calls such as run_test can legitimately take many minutes, so
    DEFAULT_HTTPX_TIME_OUT is not imposed on callers who never asked for it.
    """
    raw = os.environ.get("HTTPX_TIME_OUT")
    if not raw:
        return None
    return float(raw)


class NotJSONError(Exception):
    def __init__(self) -> None:
        super().__init__("Expected JSON response, received non-JSON.")
