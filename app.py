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
def reset(req: ResetRequest):
    global active_env
    active_env = CodeReviewEnv(task_id=req.task_id)
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
        return JSONResponse(
            status_code=400,
            content={"error": "Call /reset first."}
        )
    return active_env.step(action)