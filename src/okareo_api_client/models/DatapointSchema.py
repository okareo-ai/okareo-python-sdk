from typing import *

from pydantic import BaseModel, Field


class DatapointSchema(BaseModel):
    """
    DatapointSchema model

    """

    tags: Optional[List[str]] = Field(alias="tags", default=None)

    input: str = Field(alias="input")

    input_datetime: Optional[Union[str, Any]] = Field(alias="input_datetime", default=None)

    result: str = Field(alias="result")

    result_datetime: Optional[Union[str, Any]] = Field(alias="result_datetime", default=None)

    feedback: Optional[Union[int, Any]] = Field(alias="feedback", default=None)

    error_message: Optional[Union[str, Any]] = Field(alias="error_message", default=None)

    error_code: Optional[Union[str, Any]] = Field(alias="error_code", default=None)

    context_token: Optional[Union[str, Any]] = Field(alias="context_token", default=None)

    project_id: Optional[Union[int, Any]] = Field(alias="project_id", default=None)

    mut_id: Optional[int] = Field(alias="mut_id", default=None)
