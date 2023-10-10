from typing import *

from pydantic import BaseModel, Field


class DatapointList(BaseModel):
    """
    DatapointList model

    """

    id: int = Field(alias="id")

    tags: List[str] = Field(alias="tags")

    feedback: Optional[int] = Field(alias="feedback", default=None)

    error_message: Optional[str] = Field(alias="error_message", default=None)

    error_code: Optional[str] = Field(alias="error_code", default=None)

    time_created: str = Field(alias="time_created")

    project_id: Optional[int] = Field(alias="project_id", default=None)
