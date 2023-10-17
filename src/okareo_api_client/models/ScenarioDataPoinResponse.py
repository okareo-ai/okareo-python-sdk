from typing import *

from pydantic import BaseModel, Field


class ScenarioDataPoinResponse(BaseModel):
    """
    ScenarioDataPoinResponse model

    """

    input: str = Field(alias="input")

    result: str = Field(alias="result")

    meta_data: Optional[str] = Field(alias="meta_data", default=None)
