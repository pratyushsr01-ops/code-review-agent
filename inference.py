import os
import json
import time
import sys
from openai import OpenAI
from env.environment import CodeReviewEnv
from env.models import Action

API_BASE_URL = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "moonshotai/Kimi-K2-Instruct-0905")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

TASKS = [
    "task_1_easy_obvious_bug",
    "task_2_medium_multi_issue",
    "task_3_hard_architecture"
]

SYSTEM_PROMPT = """You are a senior software engineer doing a code review.
Analyze the pull request and return a JSON object with this exact structure:
{
  "action_type": "submit_review",
  "findings": [
    {
      "line_number": <int>,
      "category": <"bug"|"security"|"style"|"performance"|"architecture">,
      "description": "<your explanation>"
    }
  ]
}
Return ONLY the JSON. No markdown, no extra text."""

def run_task(task_id: str) -> float:
    print(f"[START] task_id={task_id} model={MODEL_NAME}")
    
    total_reward = 0.01 
    step_count = 0
    
    try:
        env = CodeReviewEnv(task_id=task_id)
        obs = env.reset()

        files_text = ""
        for f in obs.files:
            files_text += f"\n\n--- {f.filename} ---\n{f.content_with_lines}"

        user_message = f"""PR Title: {obs.pr_title}\nPR Description: {obs.pr_description}\n{files_text}\n\nReview this PR and identify all issues."""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            max_tokens=1000,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        raw = response.choices[0].message.content.strip()
        cleaned_raw = raw.replace("```json", "").replace("```", "").strip()
        data = json.loads(cleaned_raw)
        action = Action(**data)
        
        result = env.step(action)
        
        reward = result["reward"]
        done = result.get("done", True) 
        total_reward = reward
        step_count = 1
        
        print(f"[STEP] action={json.dumps(data)} reward={reward} done={done}")
        
    except Exception as e:
        print(f"[{task_id}] Error: {e}")
        total_reward = 0.01
        step_count = 1
        # Fallback log to prevent parser crash on error
        print(f"[STEP] action={{\"error\": \"{str(e)}\"}} reward=0.01 done=True")

    print(f"[END] total_reward={total_reward} steps={step_count}")
    return total_reward

if __name__ == "__main__":
    print("Running baseline inference...\n")
    total = 0.0
    for task in TASKS:
        score = run_task(task)
        total += score
        time.sleep(1) # Small delay for clean logs
        
    avg = round(total / len(TASKS), 2)
    print(f"\nAverage score: {avg}")
    sys.stdout.flush() # Forces logs to output before timeout