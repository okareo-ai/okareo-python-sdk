from typing import *

from pydantic import BaseModel, Field


class DatapointSchema(BaseModel):
    """
    DatapointSchema model

    """

    tags: Optional[List[str]] = Field(alias="tags", default=None)

    input: str = Field(alias="input")

    input_datetime: Optional[str] = Field(alias="input_datetime", default=None)

    result: str = Field(alias="result")

    result_datetime: Optional[str] = Field(alias="result_datetime", default=None)

    feedback: Optional[int] = Field(alias="feedback", default=None)

    error_message: Optional[str] = Field(alias="error_message", default=None)

    error_code: Optional[str] = Field(alias="error_code", default=None)

    context_token: Optional[str] = Field(alias="context_token", default=None)

    project_id: Optional[int] = Field(alias="project_id", default=None)

    mut_id: Optional[int] = Field(alias="mut_id", default=None)
