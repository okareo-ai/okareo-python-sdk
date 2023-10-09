from typing import *

from pydantic import BaseModel, Field


class ModelUnderTestResponse(BaseModel):
    """
    ModelUnderTestResponse model

    """

    id: int = Field(alias="id")

    project_id: int = Field(alias="project_id")

    name: str = Field(alias="name")

    tags: List[str] = Field(alias="tags")
