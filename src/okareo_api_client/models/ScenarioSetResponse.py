from typing import *

from pydantic import BaseModel, Field

from .SeedData import SeedData


class ScenarioSetResponse(BaseModel):
    """
    ScenarioSetResponse model

    """

    type: str = Field(alias="type")

    seed_data: List[SeedData] = Field(alias="seed_data")

    scenario_input: Optional[List[str]] = Field(alias="scenario_input", default=None)
