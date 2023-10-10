from typing import *

from pydantic import BaseModel, Field


class ProjectResponse(BaseModel):
    """
    ProjectResponse model

    """

    id: int = Field(alias="id")

    name: str = Field(alias="name")

    tags: Optional[List[str]] = Field(alias="tags", default=None)
