"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { CheckSquare, Plus, RefreshCw, Loader2, Pencil, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import {
  getTasks,
  createTask,
  updateTask,
  deleteTask,
  type Task,
  type TaskCreate,
} from "@/lib/tasks-api"
import { useAuth } from "@/context/auth-context"

const statusColors: Record<string, string> = {
  todo: "bg-zinc-600",
  in_progress: "bg-amber-500",
  completed: "bg-emerald-600",
}
const priorityColors: Record<string, string> = {
  high: "bg-red-500/20 text-red-400",
  medium: "bg-amber-500/20 text-amber-400",
  low: "bg-zinc-500/20 text-zinc-400",
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [newTitle, setNewTitle] = useState("")
  const [newDescription, setNewDescription] = useState("")
  const [newPriority, setNewPriority] = useState<string>("medium")
  const [filterStatus, setFilterStatus] = useState<string>("")
  const { user } = useAuth()
  const userId = user?.email ?? user?.uid ?? "me"

  const loadTasks = async () => {
    setLoading(true)
    try {
      const { tasks: list } = await getTasks(filterStatus ? { status: filterStatus } : undefined)
      setTasks(list)
    } catch {
      setTasks([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadTasks()
  }, [filterStatus])

  const handleCreate = async () => {
    if (!newTitle.trim()) return
    try {
      await createTask({
        title: newTitle.trim(),
        description: newDescription.trim() || undefined,
        priority: newPriority,
        assignee: userId,
      })
      setNewTitle("")
      setNewDescription("")
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

  const handleDelete = async (taskId: string) => {
    if (!confirm("Delete this task?")) return
    try {
      await deleteTask(taskId)
      loadTasks()
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <div className="h-full overflow-auto p-6 md:p-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <h1 className="text-2xl font-bold text-white">Tasks</h1>
          <div className="flex gap-2">
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-900 text-white text-sm"
            >
              <option value="">All statuses</option>
              <option value="todo">Todo</option>
              <option value="in_progress">In progress</option>
              <option value="completed">Completed</option>
            </select>
            <Button variant="outline" size="sm" onClick={loadTasks} className="gap-2">
              <RefreshCw className="h-4 w-4" />
              Refresh
            </Button>
          </div>
        </div>

        <Card className="p-4 border-zinc-800 bg-zinc-900/50">
          <h2 className="text-sm font-medium text-zinc-300 mb-3">Create task</h2>
          <div className="flex flex-col sm:flex-row gap-2">
            <Input
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              placeholder="Task title"
              className="flex-1 bg-zinc-800 border-zinc-700 text-white"
            />
            <Input
              value={newDescription}
              onChange={(e) => setNewDescription(e.target.value)}
              placeholder="Description (optional)"
              className="flex-1 bg-zinc-800 border-zinc-700 text-white"
            />
            <select
              value={newPriority}
              onChange={(e) => setNewPriority(e.target.value)}
              className="px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-800 text-white text-sm"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
            <Button onClick={handleCreate} className="gap-2">
              <Plus className="h-4 w-4" />
              Add
            </Button>
          </div>
        </Card>

        <Card className="p-4 border-zinc-800 bg-zinc-900/50">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-zinc-500" />
            </div>
          ) : tasks.length === 0 ? (
            <p className="text-zinc-500 text-sm py-8 text-center">No tasks. Create one above or use the Voice Agent.</p>
          ) : (
            <ScrollArea className="h-[calc(100vh-320px)]">
              <ul className="space-y-2 pr-2">
                {tasks.map((t) => (
                  <li
                    key={t.task_id}
                    className="flex items-center gap-3 p-3 rounded-lg bg-zinc-800/50 border border-zinc-700/50"
                  >
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <Link
                          href={`/dashboard/tasks/${t.task_id}`}
                          className="text-white font-medium hover:text-cyan-400 truncate"
                        >
                          {t.title}
                        </Link>
                        <Badge className={priorityColors[t.priority] ?? priorityColors.medium}>{t.priority}</Badge>
                        <span className={`text-xs px-2 py-0.5 rounded ${statusColors[t.status] ?? ""}`}>
                          {t.status}
                        </span>
                      </div>
                      {t.description && (
                        <p className="text-zinc-500 text-sm mt-1 line-clamp-1">{t.description}</p>
                      )}
                      <p className="text-zinc-600 text-xs mt-1">
                        {t.assignee}
                        {t.deadline ? ` · Due ${t.deadline.slice(0, 10)}` : ""}
                      </p>
                    </div>
                    <div className="flex items-center gap-1 shrink-0">
                      {t.status !== "completed" && (
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleStatusChange(t.task_id, t.status === "todo" ? "in_progress" : "completed")}
                        >
                          {t.status === "todo" ? "Start" : "Complete"}
                        </Button>
                      )}
                      <Link href={`/dashboard/tasks/${t.task_id}`}>
                        <Button size="sm" variant="ghost">
                          <Pencil className="h-4 w-4" />
                        </Button>
                      </Link>
                      <Button size="sm" variant="ghost" className="text-red-400 hover:text-red-300" onClick={() => handleDelete(t.task_id)}>
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </li>
                ))}
              </ul>
            </ScrollArea>
          )}
        </Card>
      </div>
    </div>
  )
}
