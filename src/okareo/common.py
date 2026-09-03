import os

DEFAULT_BASE_URL = "https://api.okareo.com"
BASE_URL = os.environ.get("OKAREO_BASE_URL") or os.environ.get(
    "BASE_URL", DEFAULT_BASE_URL
)

DEFAULT_HTTPX_TIME_OUT = 30
# being generous to support the longer generations
HTTPX_TIME_OUT = float(os.environ.get("HTTPX_TIME_OUT", DEFAULT_HTTPX_TIME_OUT))

# Client-side wall clock for `calibrate_check`, sized so the server's 504 always wins
# the race and the caller gets an answer it can act on instead of a bare local timeout.
#
# The server's own budget is 600s, but it is only checked *between* rows: the last row
# can start at 599.9s and then run a full judge call plus the one retry the pass/fail
# path makes, each capped at LLM_TIMEOUT (default 30s). So the server's real worst case
# is ~660s, not 600s, and the margin has to be one judge call plus its retry — not a
# round 30 seconds. 720 leaves headroom above that without hanging the caller for long.
# The two numbers move together: raising LLM_TIMEOUT or the server budget without
# raising this reintroduces the bare-transport-error case.
CALIBRATE_TIME_OUT = 720


class NotJSONError(Exception):
    def __init__(self) -> None:
        super().__init__("Expected JSON response, received non-JSON.")
