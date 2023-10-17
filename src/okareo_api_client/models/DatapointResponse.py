from typing import *

from pydantic import BaseModel, Field


class DatapointResponse(BaseModel):
    """
    DatapointResponse model

    """

    id: str = Field(alias="id")

    project_id: Optional[str] = Field(alias="project_id", default=None)

    mut_id: Optional[str] = Field(alias="mut_id", default=None)
