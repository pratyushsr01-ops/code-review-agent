from pydantic import BaseModel, Field, field_validator
from typing import List, Literal

class PRFile(BaseModel):
    filename: str
    content_with_lines: str

class Observation(BaseModel):
    task_id: str
    pr_title: str
    pr_description: str
    files: List[PRFile]

class Finding(BaseModel):
    line_number: int
    category: Literal["bug", "security", "style", "performance", "architecture"]
    description: str

class Action(BaseModel):
    action_type: Literal["submit_review"]
    findings: List[Finding]

class Reward(BaseModel):
    score: float = Field(..., gt=0.0, lt=1.0)
    max_score: float = Field(default=0.99, gt=0.0, lt=1.0)

    @field_validator("score", "max_score", mode="before")
    @classmethod
    def keep_scores_strictly_in_range(cls, value: float) -> float:
        numeric = float(value)
        if numeric <= 0.0:
            return 0.01
        if numeric >= 1.0:
            return 0.99
        return round(numeric, 2)
