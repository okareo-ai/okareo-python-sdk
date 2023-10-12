import os

from okareo_api_client.api_config import APIConfig

DEFAULT_BASE_URL = "https://api.okareo.com"
BASE_URL = os.environ.get("BASE_URL", DEFAULT_BASE_URL)
API_CONFIG = APIConfig(base_path=BASE_URL)
