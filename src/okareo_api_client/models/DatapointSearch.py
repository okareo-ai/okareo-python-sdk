from typing import *

from pydantic import BaseModel, Field


class DatapointSearch(BaseModel):
    """
    DatapointSearch model

    """

    tags: Optional[List[str]] = Field(alias="tags", default=None)

    from_date: Optional[str] = Field(alias="from_date", default=None)

    to_date: Optional[str] = Field(alias="to_date", default=None)

    feedback: Optional[int] = Field(alias="feedback", default=None)

    error_code: Optional[str] = Field(alias="error_code", default=None)

    context_token: Optional[str] = Field(alias="context_token", default=None)

    project_id: Optional[int] = Field(alias="project_id", default=None)

    mut_id: Optional[int] = Field(alias="mut_id", default=None)
