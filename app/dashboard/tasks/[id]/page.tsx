"use client"

import { useState, useEffect } from "react"
import { useParams, useRouter } from "next/navigation"
import Link from "next/link"
import { ArrowLeft, Loader2, Save, Trash2, Clock } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { getTask, updateTask, deleteTask, type Task, type TaskUpdate } from "@/lib/tasks-api"

export default function TaskDetailPage() {
  const params = useParams()
  const router = useRouter()
  const taskId = params.id as string
  const [task, setTask] = useState<Task | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [edit, setEdit] = useState<TaskUpdate>({})

  useEffect(() => {
    if (!taskId) return
    let cancelled = false
    getTask(taskId)
      .then((t) => {
        if (!cancelled) {
          setTask(t)
          setEdit({
            title: t.title,
            description: t.description,
            priority: t.priority,
            status: t.status,
            assignee: t.assignee,
            deadline: t.deadline ?? undefined,
          })
        }
      })
      .catch(() => {
        if (!cancelled) setTask(null)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [taskId])

  const handleSave = async () => {
    if (!taskId) return
    setSaving(true)
    try {
      await updateTask(taskId, edit)
      const updated = await getTask(taskId)
      setTask(updated)
      setEdit({
        title: updated.title,
        description: updated.description,
        priority: updated.priority,
        status: updated.status,
        assignee: updated.assignee,
        deadline: updated.deadline ?? undefined,
      })
    } catch (e) {
      console.error(e)
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async () => {
    if (!taskId || !confirm("Delete this task?")) return
    try {
      await deleteTask(taskId)
      router.push("/dashboard/tasks")
    } catch (e) {
      console.error(e)
    }
  }

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin text-zinc-500" />
      </div>
    )
  }

  if (!task) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-8 gap-4">
        <p className="text-zinc-500">Task not found.</p>
        <Link href="/dashboard/tasks">
          <Button variant="outline">Back to Tasks</Button>
        </Link>
      </div>
    )
  }

  return (
    <div className="h-full overflow-auto p-6 md:p-8">
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="flex items-center gap-4">
          <Link href="/dashboard/tasks">
            <Button variant="ghost" size="sm" className="gap-2 text-zinc-400">
              <ArrowLeft className="h-4 w-4" />
              Tasks
            </Button>
          </Link>
        </div>

        <Card className="p-6 border-zinc-800 bg-zinc-900/50 space-y-4">
          <div>
            <label className="text-xs text-zinc-500 block mb-1">Title</label>
            <Input
              value={edit.title ?? ""}
              onChange={(e) => setEdit((p) => ({ ...p, title: e.target.value }))}
              className="bg-zinc-800 border-zinc-700 text-white"
            />
          </div>
          <div>
            <label className="text-xs text-zinc-500 block mb-1">Description</label>
            <Input
              value={edit.description ?? ""}
              onChange={(e) => setEdit((p) => ({ ...p, description: e.target.value }))}
              className="bg-zinc-800 border-zinc-700 text-white"
              placeholder="Optional"
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-zinc-500 block mb-1">Status</label>
              <select
                value={edit.status ?? ""}
                onChange={(e) => setEdit((p) => ({ ...p, status: e.target.value }))}
                className="w-full px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-800 text-white text-sm"
              >
                <option value="todo">Todo</option>
                <option value="in_progress">In progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>
            <div>
              <label className="text-xs text-zinc-500 block mb-1">Priority</label>
              <select
                value={edit.priority ?? ""}
                onChange={(e) => setEdit((p) => ({ ...p, priority: e.target.value }))}
                className="w-full px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-800 text-white text-sm"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-zinc-500 block mb-1">Assignee</label>
              <Input
                value={edit.assignee ?? ""}
                onChange={(e) => setEdit((p) => ({ ...p, assignee: e.target.value }))}
                className="bg-zinc-800 border-zinc-700 text-white"
              />
            </div>
            <div>
              <label className="text-xs text-zinc-500 block mb-1">Deadline (YYYY-MM-DD)</label>
              <Input
                type="date"
                value={edit.deadline?.slice(0, 10) ?? ""}
                onChange={(e) => setEdit((p) => ({ ...p, deadline: e.target.value || undefined }))}
                className="bg-zinc-800 border-zinc-700 text-white"
              />
            </div>
          </div>
          <div className="flex items-center gap-2 pt-2">
            <Button onClick={handleSave} disabled={saving} className="gap-2">
              {saving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
              Save
            </Button>
            <Link href={`/dashboard/hours?task=${taskId}`}>
              <Button variant="outline" className="gap-2">
                <Clock className="h-4 w-4" />
                Log hours
              </Button>
            </Link>
            <Button variant="ghost" className="text-red-400 hover:text-red-300 ml-auto" onClick={handleDelete}>
              <Trash2 className="h-4 w-4" />
              Delete
            </Button>
          </div>
        </Card>

        <p className="text-zinc-600 text-xs">
          Created {task.created_at?.slice(0, 10)} · Updated {task.updated_at?.slice(0, 10)}
          {task.completed_at ? ` · Completed ${task.completed_at.slice(0, 10)}` : ""}
        </p>
      </div>
    </div>
  )
}
