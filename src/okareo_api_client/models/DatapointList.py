from typing import *

from pydantic import BaseModel, Field


class DatapointList(BaseModel):
    """
    DatapointList model

    """

    id: int = Field(alias="id")

    tags: List[str] = Field(alias="tags")

    feedback: Union[int, Any] = Field(alias="feedback")

    error_message: Union[str, Any] = Field(alias="error_message")

    error_code: Union[str, Any] = Field(alias="error_code")

    time_created: str = Field(alias="time_created")
