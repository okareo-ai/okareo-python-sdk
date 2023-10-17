from typing import *

from pydantic import BaseModel, Field


class ModelUnderTestResponse(BaseModel):
    """
    ModelUnderTestResponse model

    """

    id: str = Field(alias="id")

    project_id: str = Field(alias="project_id")

    name: str = Field(alias="name")

    tags: List[str] = Field(alias="tags")

    datapoint_count: Optional[int] = Field(alias="datapoint_count", default=None)
