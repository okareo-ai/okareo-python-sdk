from typing import *

from pydantic import BaseModel, Field


class DatapointSchema(BaseModel):
    """
    DatapointSchema model

    """

    mut_id: Optional[int] = Field(alias="mut_id", default=None)

    input: str = Field(alias="input")

    input_datetime: str = Field(alias="input_datetime")

    result: str = Field(alias="result")

    result_datetime: str = Field(alias="result_datetime")

    tags: Optional[Union[List[str], Any]] = Field(alias="tags", default=None)

    feedback: Optional[Union[int, Any]] = Field(alias="feedback", default=None)

    error_message: Optional[Union[str, Any]] = Field(alias="error_message", default=None)

    error_code: Optional[Union[str, Any]] = Field(alias="error_code", default=None)

    context_token: Optional[Union[str, Any]] = Field(alias="context_token", default=None)
