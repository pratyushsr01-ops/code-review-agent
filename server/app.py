import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
from env.environment import CodeReviewEnv
from env.models import Action

app = FastAPI(title="Code Review Agent - OpenEnv")

active_env: Optional[CodeReviewEnv] = None

class ResetRequest(BaseModel):
    task_id: Optional[str] = "task_1_easy_obvious_bug"

@app.get("/")
def root():
    return {"status": "ok", "env": "code-review-agent"}

@app.post("/reset")
def reset(req: Optional[ResetRequest] = None):
    global active_env
    task_id = "task_1_easy_obvious_bug"
    if req and req.task_id:
        task_id = req.task_id
    try:
        active_env = CodeReviewEnv(task_id=task_id)
    except KeyError:
        active_env = CodeReviewEnv(task_id="task_1_easy_obvious_bug")
    return active_env.reset().dict()

@app.get("/state")
def state():
    global active_env
    if not active_env:
        active_env = CodeReviewEnv()
    return active_env.state().dict()

@app.post("/step")
def step(action: Action):
    global active_env
    if not active_env:
        active_env = CodeReviewEnv()
    return active_env.step(action)

# --- THE FIX: ADD THESE LINES AT THE BOTTOM ---
def main():
    """The entry point required by the OpenEnv multi-mode validator."""
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()