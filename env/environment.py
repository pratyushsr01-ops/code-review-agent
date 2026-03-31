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
            return {
                "observation": self.current_obs.dict(),
                "reward": 0.0,
                "done": False,
                "info": {"message": "Invalid action type."}
            }

        score = grade(action.findings, self.expected_findings)
        self.done = True

        return {
            "observation": self.current_obs.dict(),
            "reward": score,
            "done": True,
            "info": {
                "message": f"Review complete. Score: {score}",
                "score": score
            }
        }