from typing import *

from pydantic import BaseModel, Field


class GenerationPayload(BaseModel):
    """
    GenerationPayload model

    """

    json_schema: Optional[str] = Field(alias="json_schema", default=None)

    view: str = Field(alias="view")

    return_results: Optional[bool] = Field(alias="return_results", default=None)
