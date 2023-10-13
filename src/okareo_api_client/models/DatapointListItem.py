from typing import *

from pydantic import BaseModel, Field


class DatapointListItem(BaseModel):
    """
    DatapointListItem model

    """

    id: int = Field(alias="id")

    tags: Optional[Union[List[str], Any]] = Field(alias="tags", default=None)

    feedback: Optional[Union[int, Any]] = Field(alias="feedback", default=None)

    error_message: Optional[Union[str, Any]] = Field(alias="error_message", default=None)

    error_code: Optional[Union[str, Any]] = Field(alias="error_code", default=None)

    time_created: Optional[str] = Field(alias="time_created", default=None)

    context_token: Optional[Union[str, Any]] = Field(alias="context_token", default=None)

    mut_id: Optional[int] = Field(alias="mut_id", default=None)

    project_id: Optional[int] = Field(alias="project_id", default=None)
