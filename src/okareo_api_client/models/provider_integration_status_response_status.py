from enum import Enum


class ProviderIntegrationStatusResponseStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"

    def __str__(self) -> str:
        return str(self.value)
