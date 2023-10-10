from typing import *

from pydantic import BaseModel, Field


class ModelUnderTestSchema(BaseModel):
    """
    ModelUnderTestSchema model

    """

    name: Optional[str] = Field(alias="name", default=None)

    tags: Optional[List[str]] = Field(alias="tags", default=None)

    project_id: Optional[int] = Field(alias="project_id", default=None)
