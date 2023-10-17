from typing import *

from pydantic import BaseModel, Field


class DatapointSchema(BaseModel):
    """
    DatapointSchema model

    """

    mut_id: Optional[str] = Field(alias="mut_id", default=None)

    input: Optional[str] = Field(alias="input", default=None)

    input_datetime: str = Field(alias="input_datetime")

    result: Optional[str] = Field(alias="result", default=None)

    result_datetime: str = Field(alias="result_datetime")

    tags: Optional[List[str]] = Field(alias="tags", default=None)

    feedback: Optional[int] = Field(alias="feedback", default=None)

    error_message: Optional[str] = Field(alias="error_message", default=None)

    error_code: Optional[str] = Field(alias="error_code", default=None)

    context_token: Optional[str] = Field(alias="context_token", default=None)
