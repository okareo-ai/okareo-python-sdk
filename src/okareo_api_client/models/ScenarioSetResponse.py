from typing import *

from pydantic import BaseModel, Field

from .SeedData import SeedData


class ScenarioSetResponse(BaseModel):
    """
    ScenarioSetResponse model

    """

    scenario_id: Optional[str] = Field(alias="scenario_id", default=None)

    project_id: str = Field(alias="project_id")

    time_created: str = Field(alias="time_created")

    type: str = Field(alias="type")

    tags: Optional[List[str]] = Field(alias="tags", default=None)

    name: Optional[str] = Field(alias="name", default=None)

    seed_data: Optional[List[Optional[SeedData]]] = Field(alias="seed_data", default=None)

    scenario_input: Optional[List[str]] = Field(alias="scenario_input", default=None)
