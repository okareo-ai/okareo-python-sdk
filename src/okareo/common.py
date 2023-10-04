import os

DEFAULT_BASE_URL = "https://api.okareo.com"
BASE_URL = os.environ.get("BASE_URL", DEFAULT_BASE_URL)
