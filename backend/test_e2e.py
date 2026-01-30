#!/usr/bin/env python3
"""
E2E test: backend APIs, Gemini agent, Slack webhooks (task created → #samayak-project-tasks; agent breakdown → #samyak).
Run with backend server up: uvicorn app:app --reload --port 8000
"""
import os
import sys
import json
import urllib.request
import urllib.error

BASE = os.getenv("API_BASE", "http://127.0.0.1:8001")


def req(method: str, path: str, body: dict = None) -> tuple[int, dict]:
    url = f"{BASE}{path}"
    data = json.dumps(body).encode("utf-8") if body else None
    req_obj = urllib.request.Request(url, data=data, method=method)
    req_obj.add_header("Content-Type", "application/json")
    timeout = 60 if "/api/agent" in path else 30
    try:
        with urllib.request.urlopen(req_obj, timeout=timeout) as r:
            raw = r.read().decode()
            return r.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode() if e.fp else "{}"
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"detail": raw}
    except Exception as e:
        return 0, {"error": str(e)}


def main():
    ok = 0
    fail = 0

    # 1. Health
    print("1. GET /health ...")
    code, data = req("GET", "/health")
    if code == 200 and data.get("status") in ("ok", "healthy"):
        print("   OK:", data)
        ok += 1
    else:
        print("   FAIL:", code, data)
        fail += 1

    # 2. Create task (→ Slack #samayak-project-tasks)
    print("2. POST /api/tasks (sends to Slack #samayak-project-tasks) ...")
    code, data = req("POST", "/api/tasks", {
        "title": "E2E Test: Review PR",
        "description": "Review backend PR by Friday",
        "priority": "high",
        "assignee": "shakshi@example.com",
        "tags": ["e2e", "test"],
    })
    if code == 200 and data.get("status") == "success" and data.get("task_id"):
        print("   OK: task_id =", data.get("task_id"))
        task_id = data["task_id"]
        ok += 1
    else:
        print("   FAIL:", code, data)
        fail += 1
        task_id = None

    # 3. List tasks
    print("3. GET /api/tasks ...")
    code, data = req("GET", "/api/tasks")
    if code == 200 and "tasks" in data:
        print("   OK: count =", data.get("count", len(data["tasks"])))
        ok += 1
    else:
        print("   FAIL:", code, data)
        fail += 1

    # 4. Agent process (Gemini + Slack #samyak breakdown)
    print("4. POST /api/agent/process (Gemini + Slack #samyak) ...")
    code, data = req("POST", "/api/agent/process", {
        "request": "Break down the task: Review backend PR by Friday. Give deadline and steps.",
    })
    if code == 200 and "response" in data:
        resp = data.get("response", "")[:200]
        print("   OK: response (trimmed) =", resp + "..." if len(data.get("response", "")) > 200 else resp)
        ok += 1
    else:
        print("   FAIL:", code, data)
        fail += 1

    # 5. Productivity report
    print("5. GET /api/productivity/report ...")
    code, data = req("GET", "/api/productivity/report?days=7")
    if code == 200 and "total_tasks" in data:
        print("   OK: total_tasks =", data.get("total_tasks"), "completion_rate =", data.get("completion_rate"))
        ok += 1
    else:
        print("   FAIL:", code, data)
        fail += 1

    # 6. Update task status (→ Slack on completed)
    if task_id:
        print("6. PATCH /api/tasks/... status=completed (Slack #samayak-project-tasks) ...")
        code, data = req("PATCH", f"/api/tasks/{task_id}", {"status": "completed"})
        if code == 200:
            print("   OK")
            ok += 1
        else:
            print("   FAIL:", code, data)
            fail += 1

    print()
    print("--- Result: %d passed, %d failed ---" % (ok, fail))
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
