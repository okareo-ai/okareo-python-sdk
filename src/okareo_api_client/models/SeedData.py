from typing import *

from pydantic import BaseModel, Field


class SeedData(BaseModel):
    """
    SeedData model

    """

    input: str = Field(alias="input")

    result: str = Field(alias="result")
