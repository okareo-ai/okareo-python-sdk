from typing import *

from pydantic import BaseModel, Field


class ProjectSchema(BaseModel):
    """
    ProjectSchema model

    """

    name: Optional[str] = Field(alias="name", default=None)

    tags: Optional[Union[List[str], Any]] = Field(alias="tags", default=None)
