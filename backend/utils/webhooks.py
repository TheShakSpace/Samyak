"""Optional webhooks: task assignments → #samayak-project-tasks; agent breakdowns → #samyak."""
import json
from typing import Optional, Dict, Any
from config import (
    WEBHOOK_URL_SLACK_TASKS,
    WEBHOOK_URL_SLACK_AGENT,
    WEBHOOK_URL_SLACK,
    WEBHOOK_URL_DISCORD,
    WEBHOOK_URL_TEAMS,
)


def _post(url: str, payload: Dict[str, Any]) -> bool:
    try:
        import urllib.request
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as _:
            return True
    except Exception:
        return False


def notify_task_event(event: str, task_id: str, title: str, assignee: str = "", extra: Optional[dict] = None):
    """Send task assignment/update to #samayak-project-tasks (or fallback Slack webhook)."""
    text = f"[{event}] Task {task_id}: {title}" + (f" (assignee: {assignee})" if assignee else "")
    payload_slack = {"text": text}
    payload_discord = {"content": text}
    payload_teams = {"@type": "MessageCard", "text": text}
    url_tasks = WEBHOOK_URL_SLACK_TASKS or WEBHOOK_URL_SLACK
    if url_tasks:
        _post(url_tasks, payload_slack)
    if WEBHOOK_URL_DISCORD:
        _post(WEBHOOK_URL_DISCORD, payload_discord)
    if WEBHOOK_URL_TEAMS:
        _post(WEBHOOK_URL_TEAMS, payload_teams)


def notify_agent_breakdown(message: str, title: Optional[str] = None):
    """Send Gemini agent breakdown/summary to #samyak (deadline, how to do it, etc.)."""
    if not WEBHOOK_URL_SLACK_AGENT:
        return
    header = title or "Agent breakdown"
    text = f"*{header}*\n\n{message}"
    payload = {"text": text}
    _post(WEBHOOK_URL_SLACK_AGENT, payload)
