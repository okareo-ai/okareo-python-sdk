from typing import *

from pydantic import BaseModel, Field

from .SeedData import SeedData


class ScenarioSetCreate(BaseModel):
    """
    ScenarioSetCreate model

    """

    project_id: Optional[str] = Field(alias="project_id", default=None)

    name: str = Field(alias="name")

    seed_data: List[SeedData] = Field(alias="seed_data")

    number_examples: int = Field(alias="number_examples")
