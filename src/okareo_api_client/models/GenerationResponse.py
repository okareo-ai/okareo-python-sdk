from typing import *

from pydantic import BaseModel, Field


class GenerationResponse(BaseModel):
    """
    GenerationResponse model

    """

    hash: str = Field(alias="hash")

    data: str = Field(alias="data")
