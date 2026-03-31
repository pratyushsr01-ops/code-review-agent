---
title: Code Review Agent
emoji: 🔍
colorFrom: blue
colorTo: purple
sdk: docker
tags:
  - openenv
license: mit
---

# Code Review Agent — OpenEnv

An environment where an AI agent reviews Pull Requests and identifies bugs,
security issues, and architectural problems.

## API Endpoints
- `GET /` — health check
- `POST /reset` — start a task `{"task_id": "task_1_easy_obvious_bug"}`
- `GET /state?task_id=...` — current observation
- `POST /step?task_id=...` — submit a review

## Tasks
| Task | Difficulty | Issues to find |
|------|-----------|----------------|
| task_1_easy_obvious_bug | Easy | 1 — off-by-one in range() |
| task_2_medium_multi_issue | Medium | 3 — unused import, SQL injection, None comparison |
| task_3_hard_architecture | Hard | 2 — N+1 query, commit ordering bug |

## Reward
Partial credit per issue: `score = matched / total` (0.0–1.0)

## Baseline Scores
| Task | Score |
|------|-------|
| task_1 | 1.0 |
| task_2 | 0.67 |
| task_3 | 0.5 |
| **Average** | **0.72** |

## Setup
```bash
docker build -t code-review-agent .
docker run -p 7860:7860 \
  -e HF_TOKEN=your_token \
  -e API_BASE_URL=https://router.huggingface.co/v1 \
  -e MODEL_NAME=moonshotai/Kimi-K2-Instruct-0905 \
  code-review-agent
```
