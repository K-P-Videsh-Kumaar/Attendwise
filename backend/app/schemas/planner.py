from pydantic import BaseModel, Field


class ScenarioItem(BaseModel):
    subject_id: int
    attended: int = Field(default=0, ge=0)
    missed: int = Field(default=0, ge=0)


class SimulateIn(BaseModel):
    scenarios: list[ScenarioItem] = Field(min_length=1)
