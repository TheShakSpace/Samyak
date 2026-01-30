"""
FastAPI server for Agentic Task & Management (Remote Team Productivity).
REST API: tasks, working hours, productivity report, agent.
"""
import os
from datetime import datetime, timedelta
from typing import Optional, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import after env is loaded
from config import (
    BACKEND_BASE_URL,
    WEBHOOK_URL_SLACK_TASKS,
    WEBHOOK_URL_SLACK_AGENT,
    WEBHOOK_URL_SLACK,
    GOOGLE_OAUTH_CLIENT_ID,
)
from db.factory import get_task_manager_factory
from db.firebase import get_hours_repository
from models.task import Task
from models.working_hours import WorkingHours
from tools.task_tools import (
    create_task as tool_create_task,
    update_task_status as tool_update_status,
    get_all_tasks as tool_get_all_tasks,
    delete_task as tool_delete_task,
    calculate_productivity_metrics,
)
from tools.hours_tools import log_working_hours as tool_log_hours, get_working_hours as tool_get_hours
from agent.orchestrator import TaskManagementAgent
from utils.webhooks import notify_task_event, notify_agent_breakdown


# --- Pydantic models ---
class TaskCreate(BaseModel):
    title: str
    description: str = ""
    priority: str = "medium"
    deadline: Optional[str] = None
    assignee: str = "me"
    tags: List[str] = []


class TaskUpdate(BaseModel):
    status: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    deadline: Optional[str] = None
    assignee: Optional[str] = None
    tags: Optional[List[str]] = None


class WorkingHoursCreate(BaseModel):
    task_id: str
    user_id: str
    minutes: int = Field(..., gt=0)
    date: Optional[str] = None
    notes: str = ""


class AgentRequest(BaseModel):
    request: str


# --- App ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure task manager can be created (lazy Firebase init on first request is ok)
    yield
    # Shutdown
    pass


app = FastAPI(
    title="Agentic Task & Management API",
    description="Remote Team Task and Productivity Tracker",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Tasks ---
@app.get("/api/tasks")
def list_tasks(
    status: Optional[str] = Query(None),
    assignee: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
):
    result = tool_get_all_tasks(status=status, assignee=assignee, tag=tag)
    return result


@app.get("/api/tasks/{task_id}")
def get_task(task_id: str):
    tm = get_task_manager_factory()
    task = tm.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.to_dict()


@app.post("/api/tasks")
def create_task(body: TaskCreate):
    result = tool_create_task(
        title=body.title,
        description=body.description,
        priority=body.priority,
        deadline=body.deadline,
        assignee=body.assignee,
        tags=body.tags if body.tags else None,
    )
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message", "Error"))
    notify_task_event("created", result["task_id"], body.title, body.assignee)
    return result


@app.patch("/api/tasks/{task_id}")
def update_task(task_id: str, body: TaskUpdate):
    tm = get_task_manager_factory()
    task = tm.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    updates = body.model_dump(exclude_unset=True)
    if "status" in updates:
        result = tool_update_status(task_id, updates["status"])
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        if updates["status"] == "completed":
            notify_task_event("completed", task_id, task.title, task.assignee)
    for key in ["title", "description", "priority", "deadline", "assignee", "tags"]:
        if key in updates and updates[key] is not None:
            tm.update_task(task_id, **{key: updates[key]})
    task = tm.get_task(task_id)
    return {"status": "success", "task": task.to_dict()}


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: str):
    result = tool_delete_task(task_id)
    if result.get("status") == "error":
        raise HTTPException(status_code=404, detail=result.get("message", "Not found"))
    return result


# --- Working hours ---
@app.post("/api/working-hours")
def log_working_hours(body: WorkingHoursCreate):
    result = tool_log_hours(
        task_id=body.task_id,
        user_id=body.user_id,
        minutes=body.minutes,
        date=body.date,
        notes=body.notes,
    )
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message", "Error"))
    return result


@app.get("/api/working-hours")
def list_working_hours(
    task_id: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    from_date: Optional[str] = Query(None),
    to_date: Optional[str] = Query(None),
):
    result = tool_get_hours(task_id=task_id, user_id=user_id, from_date=from_date, to_date=to_date)
    return result


# --- Productivity report ---
@app.get("/api/productivity/report")
def productivity_report(
    assignee: Optional[str] = Query(None),
    days: int = Query(30, ge=1, le=365),
):
    result = calculate_productivity_metrics(assignee=assignee, days=days)
    repo = get_hours_repository()
    if repo:
        from_d = datetime.now().date() - timedelta(days=days)
        to_d = datetime.now().date()
        entries = repo.list_by_date_range(from_d, to_d, user_id=assignee if assignee and assignee != "all" else None)
        total_minutes = sum(e.minutes for e in entries)
        result["total_minutes_logged"] = total_minutes
        result["total_hours_logged"] = round(total_minutes / 60, 2)
    return result


# --- Agent ---
_agent: Optional[TaskManagementAgent] = None


def get_agent() -> TaskManagementAgent:
    global _agent
    if _agent is None:
        _agent = TaskManagementAgent()
    return _agent


@app.post("/api/agent/process")
def agent_process(body: AgentRequest):
    agent = get_agent()
    result = agent.process_request(body.request, use_llm=True)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message", "Agent error"))
    response_text = result.get("response", result.get("message", ""))
    # Send agent breakdown to #samyak (Gemini summary, deadline, how to do it)
    if response_text:
        notify_agent_breakdown(response_text, title="Task breakdown")
    return {"response": response_text, "routing": result.get("routing", {})}


@app.get("/health")
def health():
    return {"status": "ok", "service": "agentic-task-api"}


@app.get("/api/integrations/status")
def integrations_status():
    """Return which integrations are configured (no secrets). Frontend uses this for Slack/Calendar status."""
    slack_tasks = bool(WEBHOOK_URL_SLACK_TASKS or WEBHOOK_URL_SLACK)
    slack_agent = bool(WEBHOOK_URL_SLACK_AGENT)
    google_oauth = bool(GOOGLE_OAUTH_CLIENT_ID)
    return {
        "slack_tasks": slack_tasks,
        "slack_agent": slack_agent,
        "google_oauth": google_oauth,
        "calendar_sync": False,  # Not implemented yet
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
