import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
from pydantic import BaseModel
from env.environment import CodeReviewEnv
from env.graders import MIN_STRICT_SCORE, sanitize_score
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

# Catch unexpected crashes and return a safe fallback score
@app.post("/step")
async def step(request: Request):
    global active_env
    if not active_env:
        active_env = CodeReviewEnv()
    
    try:
        # Manually parse the JSON to intercept FastAPI crashes
        body = await request.json()
        action = Action(**body)
        return active_env.step(action)
    except Exception as e:
        # Handle invalid requests gracefully
        active_env.done = True
        obs_dict = active_env.current_obs.dict() if hasattr(active_env, 'current_obs') else {}
        return {
            "observation": obs_dict,
            "reward": MIN_STRICT_SCORE,
            "done": True,
            "info": {
                "message": f"Server caught exception: {str(e)}",
                "score": sanitize_score(MIN_STRICT_SCORE)
            }
        }

def main():
    """The entry point required by the OpenEnv multi-mode validator."""
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
