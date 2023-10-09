from typing import *

from pydantic import BaseModel, Field


class ProjectResponse(BaseModel):
    """
    ProjectResponse model

    """

    id: int = Field(alias="id")

    name: str = Field(alias="name")

    tags: Union[List[str], Any] = Field(alias="tags")
