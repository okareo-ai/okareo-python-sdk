from typing import *

from pydantic import BaseModel, Field


class GenerationList(BaseModel):
    """
    GenerationList model

    """

    hash: str = Field(alias="hash")

    time_created: str = Field(alias="time_created")
