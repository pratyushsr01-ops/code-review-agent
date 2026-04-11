from pydantic import BaseModel
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
    score: float
    max_score: float = 0.99
