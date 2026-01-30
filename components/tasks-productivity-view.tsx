"use client"

import { useState, useEffect } from "react"
import { CheckSquare, Clock, BarChart3, Plus, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  getTasks,
  createTask,
  updateTask,
  deleteTask,
  logWorkingHours,
  getWorkingHours,
  getProductivityReport,
  type Task,
  type TaskCreate,
  type ProductivityReport,
} from "@/lib/tasks-api"
import { useAuth } from "@/context/auth-context"

type Tab = "tasks" | "hours" | "report"

export default function TasksProductivityView() {
  const [tab, setTab] = useState<Tab>("tasks")
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [report, setReport] = useState<ProductivityReport | null>(null)
  const [newTitle, setNewTitle] = useState("")
  const [logTaskId, setLogTaskId] = useState("")
  const [logMinutes, setLogMinutes] = useState("")
  const { user } = useAuth()
  const userId = user?.email ?? user?.uid ?? "me"

  const loadTasks = async () => {
    setLoading(true)
    try {
      const { tasks: list } = await getTasks()
      setTasks(list)
    } catch (e) {
      console.error(e)
      setTasks([])
    } finally {
      setLoading(false)
    }
  }

  const loadReport = async () => {
    try {
      const r = await getProductivityReport({ days: 30 })
      setReport(r)
    } catch (e) {
      console.error(e)
      setReport(null)
    }
  }

  useEffect(() => {
    loadTasks()
  }, [])

  useEffect(() => {
    if (tab === "report") loadReport()
  }, [tab])

  const handleCreateTask = async () => {
    if (!newTitle.trim()) return
    try {
      await createTask({ title: newTitle.trim(), assignee: userId })
      setNewTitle("")
      loadTasks()
    } catch (e) {
      console.error(e)
    }
  }

  const handleStatusChange = async (taskId: string, status: string) => {
    try {
      await updateTask(taskId, { status })
      loadTasks()
    } catch (e) {
      console.error(e)
    }
  }

  const handleLogHours = async () => {
    if (!logTaskId || !logMinutes || parseInt(logMinutes, 10) <= 0) return
    try {
      await logWorkingHours({
        task_id: logTaskId,
        user_id: userId,
        minutes: parseInt(logMinutes, 10),
      })
      setLogTaskId("")
      setLogMinutes("")
      loadTasks()
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <div className="h-full p-4 sm:p-6 space-y-4 overflow-auto">
      <div className="flex items-center gap-2 flex-wrap">
        <Button
          variant={tab === "tasks" ? "default" : "outline"}
          size="sm"
          onClick={() => setTab("tasks")}
          className="gap-2"
        >
          <CheckSquare className="h-4 w-4" />
          Tasks
        </Button>
        <Button
          variant={tab === "hours" ? "default" : "outline"}
          size="sm"
          onClick={() => setTab("hours")}
          className="gap-2"
        >
          <Clock className="h-4 w-4" />
          Log Hours
        </Button>
        <Button
          variant={tab === "report" ? "default" : "outline"}
          size="sm"
          onClick={() => setTab("report")}
          className="gap-2"
        >
          <BarChart3 className="h-4 w-4" />
          Productivity
        </Button>
        <Button variant="ghost" size="sm" onClick={loadTasks} className="gap-2 ml-auto">
          <RefreshCw className="h-4 w-4" />
          Refresh
        </Button>
      </div>

      {tab === "tasks" && (
        <Card className="p-4 border-primary/20">
          <div className="flex gap-2 mb-4">
            <input
              type="text"
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleCreateTask()}
              placeholder="New task title..."
              className="flex-1 px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-900 text-white text-sm"
            />
            <Button size="sm" onClick={handleCreateTask} className="gap-1">
              <Plus className="h-4 w-4" />
              Add
            </Button>
          </div>
          {loading ? (
            <p className="text-zinc-400 text-sm">Loading tasks...</p>
          ) : tasks.length === 0 ? (
            <p className="text-zinc-500 text-sm">No tasks yet. Create one above or use the Agent.</p>
          ) : (
            <ScrollArea className="h-[400px]">
              <div className="space-y-2 pr-2">
                {tasks.map((t) => (
                  <div
                    key={t.task_id}
                    className="flex items-center justify-between p-3 rounded-lg bg-zinc-800/50 border border-zinc-700/50"
                  >
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-medium text-white truncate">{t.title}</p>
                      <p className="text-xs text-zinc-500">
                        {t.status} · {t.priority} · {t.assignee}
                        {t.deadline ? ` · Due ${t.deadline.slice(0, 10)}` : ""}
                      </p>
                    </div>
                    <div className="flex gap-1 flex-shrink-0">
                      {t.status !== "completed" && (
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleStatusChange(t.task_id, t.status === "todo" ? "in_progress" : "completed")}
                        >
                          {t.status === "todo" ? "Start" : "Complete"}
                        </Button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </ScrollArea>
          )}
        </Card>
      )}

      {tab === "hours" && (
        <Card className="p-4 border-primary/20">
          <p className="text-sm text-zinc-400 mb-3">Log working time for a task (backend must support working hours / Firebase).</p>
          <div className="flex flex-wrap gap-2 items-end">
            <div>
              <label className="text-xs text-zinc-500 block mb-1">Task ID</label>
              <input
                type="text"
                value={logTaskId}
                onChange={(e) => setLogTaskId(e.target.value)}
                placeholder="e.g. TASK001"
                className="w-40 px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-900 text-white text-sm"
              />
            </div>
            <div>
              <label className="text-xs text-zinc-500 block mb-1">Minutes</label>
              <input
                type="number"
                value={logMinutes}
                onChange={(e) => setLogMinutes(e.target.value)}
                min={1}
                placeholder="30"
                className="w-24 px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-900 text-white text-sm"
              />
            </div>
            <Button size="sm" onClick={handleLogHours}>
              Log
            </Button>
          </div>
          {tasks.length > 0 && (
            <p className="text-xs text-zinc-500 mt-2">
              Task IDs: {tasks.slice(0, 5).map((t) => t.task_id).join(", ")}
              {tasks.length > 5 ? "..." : ""}
            </p>
          )}
        </Card>
      )}

      {tab === "report" && (
        <Card className="p-4 border-primary/20">
          {report === null ? (
            <p className="text-zinc-500 text-sm">Loading report...</p>
          ) : (
            <div className="space-y-3 text-sm">
              <p className="text-zinc-400">
                Last {report.period_days} days · Assignee: {report.assignee}
              </p>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="p-3 rounded-lg bg-zinc-800/50">
                  <p className="text-zinc-500 text-xs">Total tasks</p>
                  <p className="text-white font-medium">{report.total_tasks}</p>
                </div>
                <div className="p-3 rounded-lg bg-zinc-800/50">
                  <p className="text-zinc-500 text-xs">Completion rate</p>
                  <p className="text-white font-medium">{report.completion_rate}%</p>
                </div>
                <div className="p-3 rounded-lg bg-zinc-800/50">
                  <p className="text-zinc-500 text-xs">Completed</p>
                  <p className="text-white font-medium">{report.status_breakdown.completed}</p>
                </div>
                <div className="p-3 rounded-lg bg-zinc-800/50">
                  <p className="text-zinc-500 text-xs">Hours logged</p>
                  <p className="text-white font-medium">{report.total_hours_logged ?? 0}</p>
                </div>
              </div>
            </div>
          )}
        </Card>
      )}
    </div>
  )
}
