from .models import Observation, Action
from .tasks import TASKS
from .graders import grade
from typing import Dict, Any

class CodeReviewEnv:

    def __init__(self, task_id: str = "task_1_easy_obvious_bug"):
        self.task_id = task_id
        self.done = False
        self.reset()

    def reset(self) -> Observation:
        self.done = False
        task = TASKS[self.task_id]
        self.current_obs = Observation(
            task_id=self.task_id,
            pr_title=task["pr_title"],
            pr_description=task["pr_description"],
            files=task["files"]
        )
        self.expected_findings = task["expected_findings"]
        return self.current_obs

    def state(self) -> Observation:
        return self.current_obs

    def step(self, action: Action) -> Dict[str, Any]:
        
        if action.action_type != "submit_review":
            self.done = True
            return {
                "observation": self.current_obs.dict(),
                "reward": 0.01,
                "done": True, 
                "info": {
                    "message": "Invalid action type.",
                    "score": 0.01 
                }
            }

        # 1. Get the score from the grader
        raw_score = grade(action.findings, self.expected_findings)
        
        safe_score = float(max(0.01, min(0.99, raw_score)))
        
        self.done = True

        return {
            "observation": self.current_obs.dict(),
            "reward": safe_score,
            "done": True,
            "info": {
                "message": f"Review complete. Score: {safe_score}",
                "score": safe_score
            }
        }