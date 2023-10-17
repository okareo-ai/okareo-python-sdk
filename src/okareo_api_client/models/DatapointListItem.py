from typing import *

from pydantic import BaseModel, Field


class DatapointListItem(BaseModel):
    """
    DatapointListItem model

    """

    id: str = Field(alias="id")

    tags: Optional[List[str]] = Field(alias="tags", default=None)

    feedback: Optional[int] = Field(alias="feedback", default=None)

    error_message: Optional[str] = Field(alias="error_message", default=None)

    error_code: Optional[str] = Field(alias="error_code", default=None)

    time_created: Optional[str] = Field(alias="time_created", default=None)

    context_token: Optional[str] = Field(alias="context_token", default=None)

    mut_id: Optional[str] = Field(alias="mut_id", default=None)

    project_id: Optional[str] = Field(alias="project_id", default=None)
