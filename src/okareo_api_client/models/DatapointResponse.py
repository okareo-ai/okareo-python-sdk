from typing import *

from pydantic import BaseModel, Field


class DatapointResponse(BaseModel):
    """
    DatapointResponse model

    """

    id: int = Field(alias="id")

    project_id: Optional[Union[int, Any]] = Field(alias="project_id", default=None)

    mut_id: Optional[int] = Field(alias="mut_id", default=None)
