/**
 * Backend API client for Agentic Task & Management (tasks, working hours, productivity).
 * In browser we use same-origin "" so Next.js rewrites /api/* to the backend (see next.config.mjs).
 */
const API_BASE =
  typeof window !== "undefined"
    ? "" // same-origin; Next.js rewrites /api/* to backend
    : (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000")

function authHeaders(): HeadersInit {
  const token = typeof window !== "undefined" ? localStorage.getItem("samyak_auth_token") : null
  const headers: HeadersInit = { "Content-Type": "application/json" }
  if (token) (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`
  return headers
}

export interface Task {
  task_id: string
  title: string
  description: string
  priority: string
  deadline: string | null
  status: string
  assignee: string
  tags: string[]
  created_at: string
  updated_at: string
  completed_at: string | null
}

export interface TaskCreate {
  title: string
  description?: string
  priority?: string
  deadline?: string | null
  assignee?: string
  tags?: string[]
}

export interface TaskUpdate {
  status?: string
  title?: string
  description?: string
  priority?: string
  deadline?: string | null
  assignee?: string
  tags?: string[]
}

export interface WorkingHoursEntry {
  id: string
  task_id: string
  user_id: string
  minutes: number
  date: string
  notes: string
  created_at: string
}

export interface WorkingHoursCreate {
  task_id: string
  user_id: string
  minutes: number
  date?: string | null
  notes?: string
}

export interface ProductivityReport {
  period_days: number
  assignee: string
  total_tasks: number
  status_breakdown: { completed: number; in_progress: number; todo: number }
  priority_breakdown: { high: number; medium: number; low: number }
  completion_rate: number
  average_completion_hours: number | null
  total_minutes_logged?: number
  total_hours_logged?: number
}

// --- Tasks ---
export async function getTasks(params?: {
  status?: string
  assignee?: string
  tag?: string
}): Promise<{ count: number; tasks: Task[] }> {
  const q = new URLSearchParams()
  if (params?.status) q.set("status", params.status)
  if (params?.assignee) q.set("assignee", params.assignee)
  if (params?.tag) q.set("tag", params.tag)
  const url = `${API_BASE}/api/tasks${q.toString() ? `?${q}` : ""}`
  const res = await fetch(url, { headers: authHeaders() })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.detail || "Failed to fetch tasks")
  return { count: data.count ?? data.tasks?.length ?? 0, tasks: data.tasks ?? [] }
}

export async function getTask(taskId: string): Promise<Task> {
  const res = await fetch(`${API_BASE}/api/tasks/${taskId}`, { headers: authHeaders() })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.detail || "Task not found")
  return data
}

export async function createTask(body: TaskCreate): Promise<{ task_id: string; task: Task }> {
  const res = await fetch(`${API_BASE}/api/tasks`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(body),
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.detail || "Failed to create task")
  return { task_id: data.task_id, task: data.task }
}

export async function updateTask(
  taskId: string,
  body: TaskUpdate
): Promise<{ status: string; task: Task }> {
  const res = await fetch(`${API_BASE}/api/tasks/${taskId}`, {
    method: "PATCH",
    headers: authHeaders(),
    body: JSON.stringify(body),
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.detail || "Failed to update task")
  return data
}

export async function deleteTask(taskId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/api/tasks/${taskId}`, {
    method: "DELETE",
    headers: authHeaders(),
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.detail || "Failed to delete task")
}

// --- Working hours ---
export async function logWorkingHours(
  body: WorkingHoursCreate
): Promise<{ status: string; working_hours: WorkingHoursEntry }> {
  const res = await fetch(`${API_BASE}/api/working-hours`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(body),
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.detail || "Failed to log hours")
  return data
}

export async function getWorkingHours(params?: {
  task_id?: string
  user_id?: string
  from_date?: string
  to_date?: string
}): Promise<{ count: number; entries: WorkingHoursEntry[] }> {
  const q = new URLSearchParams()
  if (params?.task_id) q.set("task_id", params.task_id)
  if (params?.user_id) q.set("user_id", params.user_id)
  if (params?.from_date) q.set("from_date", params.from_date)
  if (params?.to_date) q.set("to_date", params.to_date)
  const url = `${API_BASE}/api/working-hours${q.toString() ? `?${q}` : ""}`
  const res = await fetch(url, { headers: authHeaders() })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.detail || "Failed to fetch working hours")
  return { count: data.count ?? 0, entries: data.entries ?? [] }
}

// --- Productivity ---
export async function getProductivityReport(params?: {
  assignee?: string
  days?: number
}): Promise<ProductivityReport> {
  const q = new URLSearchParams()
  if (params?.assignee) q.set("assignee", params.assignee)
  if (params?.days) q.set("days", String(params.days))
  const url = `${API_BASE}/api/productivity/report${q.toString() ? `?${q}` : ""}`
  const res = await fetch(url, { headers: authHeaders() })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.detail || "Failed to fetch report")
  return data
}

// --- Agent ---
export async function processAgentRequest(request: string): Promise<{
  response: string
  routing?: Record<string, unknown>
}> {
  const res = await fetch(`${API_BASE}/api/agent/process`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ request }),
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.detail || "Agent request failed")
  return data
}

// --- Integrations (Slack, Gmail/Calendar) ---
export interface IntegrationsStatus {
  slack_tasks: boolean
  slack_agent: boolean
  google_oauth: boolean
  calendar_sync: boolean
}

export async function getIntegrationsStatus(): Promise<IntegrationsStatus> {
  const res = await fetch(`${API_BASE}/api/integrations/status`, { headers: authHeaders() })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) return { slack_tasks: false, slack_agent: false, google_oauth: false, calendar_sync: false }
  return {
    slack_tasks: !!data.slack_tasks,
    slack_agent: !!data.slack_agent,
    google_oauth: !!data.google_oauth,
    calendar_sync: !!data.calendar_sync,
  }
}
