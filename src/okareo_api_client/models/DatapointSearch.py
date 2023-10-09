from typing import *

from pydantic import BaseModel, Field


class DatapointSearch(BaseModel):
    """
    DatapointSearch model

    """

    tags: Optional[List[str]] = Field(alias="tags", default=None)

    from_date: Optional[Union[str, Any]] = Field(alias="from_date", default=None)

    to_date: Optional[Union[str, Any]] = Field(alias="to_date", default=None)

    feedback: Optional[Union[int, Any]] = Field(alias="feedback", default=None)

    error_code: Optional[Union[str, Any]] = Field(alias="error_code", default=None)

    context_token: Optional[Union[str, Any]] = Field(alias="context_token", default=None)

    project_id: Optional[Union[int, Any]] = Field(alias="project_id", default=None)

    mut_id: Optional[Union[int, Any]] = Field(alias="mut_id", default=None)
