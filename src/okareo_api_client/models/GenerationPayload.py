from typing import *

from pydantic import BaseModel, Field


class GenerationPayload(BaseModel):
    """
    GenerationPayload model

    """

    schema: str = Field(alias="schema")

    view: str = Field(alias="view")

    return_results: Optional[bool] = Field(alias="return_results", default=None)
