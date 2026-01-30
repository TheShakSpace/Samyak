"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { UserCheck, Loader2, RefreshCw, CheckSquare, Clock } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { getTasks, updateTask, type Task } from "@/lib/tasks-api"
import { useAuth } from "@/context/auth-context"

const statusColors: Record<string, string> = {
  todo: "bg-zinc-600",
  in_progress: "bg-amber-500",
  completed: "bg-emerald-600",
}

export default function MyWorkPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const { user } = useAuth()
  const userId = user?.email ?? user?.uid ?? "me"

  const loadTasks = async () => {
    setLoading(true)
    try {
      const { tasks: list } = await getTasks({ assignee: userId })
      setTasks(list)
    } catch {
      setTasks([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadTasks()
  }, [userId])

  const handleStatusChange = async (taskId: string, status: string) => {
    try {
      await updateTask(taskId, { status })
      loadTasks()
    } catch (e) {
      console.error(e)
    }
  }

  const todo = tasks.filter((t) => t.status === "todo")
  const inProgress = tasks.filter((t) => t.status === "in_progress")
  const completed = tasks.filter((t) => t.status === "completed")

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin text-zinc-500" />
      </div>
    )
  }

  return (
    <div className="h-full overflow-auto p-6 md:p-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <h1 className="text-2xl font-bold text-white">My work</h1>
          <Button variant="outline" size="sm" onClick={loadTasks} className="gap-2">
            <RefreshCw className="h-4 w-4" />
            Refresh
          </Button>
        </div>
        <p className="text-zinc-400 text-sm">
          Tasks assigned to you. Quick status updates and links to details.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <Card className="p-4 border-zinc-800 bg-zinc-900/50">
            <div className="flex items-center gap-2 mb-2">
              <CheckSquare className="h-4 w-4 text-zinc-500" />
              <span className="text-zinc-400 text-sm">Todo</span>
            </div>
            <p className="text-2xl font-bold text-white">{todo.length}</p>
          </Card>
          <Card className="p-4 border-zinc-800 bg-zinc-900/50">
            <div className="flex items-center gap-2 mb-2">
              <Clock className="h-4 w-4 text-amber-500" />
              <span className="text-zinc-400 text-sm">In progress</span>
            </div>
            <p className="text-2xl font-bold text-white">{inProgress.length}</p>
          </Card>
          <Card className="p-4 border-zinc-800 bg-zinc-900/50">
            <div className="flex items-center gap-2 mb-2">
              <UserCheck className="h-4 w-4 text-emerald-500" />
              <span className="text-zinc-400 text-sm">Completed</span>
            </div>
            <p className="text-2xl font-bold text-white">{completed.length}</p>
          </Card>
        </div>

        <Card className="p-4 border-zinc-800 bg-zinc-900/50">
          {tasks.length === 0 ? (
            <p className="text-zinc-500 text-sm py-6 text-center">No tasks assigned to you yet.</p>
          ) : (
            <ul className="space-y-2">
              {tasks.map((t) => (
                <li
                  key={t.task_id}
                  className="flex items-center justify-between p-3 rounded-lg bg-zinc-800/50 border border-zinc-700/50"
                >
                  <Link href={`/dashboard/tasks/${t.task_id}`} className="flex-1 min-w-0">
                    <p className="text-white font-medium truncate hover:text-cyan-400">{t.title}</p>
                    <p className="text-zinc-500 text-xs mt-0.5">
                      {t.priority} · {t.deadline ? `Due ${t.deadline.slice(0, 10)}` : "No deadline"}
                    </p>
                  </Link>
                  <div className="flex items-center gap-2 shrink-0">
                    <span className={`text-xs px-2 py-0.5 rounded ${statusColors[t.status] ?? ""}`}>
                      {t.status}
                    </span>
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
                </li>
              ))}
            </ul>
          )}
        </Card>
      </div>
    </div>
  )
}
