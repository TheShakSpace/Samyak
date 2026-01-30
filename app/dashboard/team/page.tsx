"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Users, Loader2, RefreshCw, ChevronRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { getTasks, type Task } from "@/lib/tasks-api"

function groupByAssignee(tasks: Task[]): Record<string, Task[]> {
  const map: Record<string, Task[]> = {}
  for (const t of tasks) {
    const key = t.assignee || "Unassigned"
    if (!map[key]) map[key] = []
    map[key].push(t)
  }
  return map
}

export default function TeamPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)

  const loadTasks = async () => {
    setLoading(true)
    try {
      const { tasks: list } = await getTasks()
      setTasks(list)
    } catch {
      setTasks([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadTasks()
  }, [])

  const byAssignee = groupByAssignee(tasks)
  const assignees = Object.keys(byAssignee).sort()

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
          <h1 className="text-2xl font-bold text-white">Team</h1>
          <Button variant="outline" size="sm" onClick={loadTasks} className="gap-2">
            <RefreshCw className="h-4 w-4" />
            Refresh
          </Button>
        </div>
        <p className="text-zinc-400 text-sm">
          Tasks grouped by assignee. Use this view to see workload and who is working on what.
        </p>

        {assignees.length === 0 ? (
          <Card className="p-8 border-zinc-800 bg-zinc-900/50 text-center">
            <Users className="h-12 w-12 text-zinc-600 mx-auto mb-3" />
            <p className="text-zinc-500">No tasks yet. Create tasks and assign them to see the team view.</p>
          </Card>
        ) : (
          <div className="space-y-4">
            {assignees.map((assignee) => {
              const list = byAssignee[assignee]
              const todo = list.filter((t) => t.status === "todo").length
              const inProgress = list.filter((t) => t.status === "in_progress").length
              const completed = list.filter((t) => t.status === "completed").length
              return (
                <Card key={assignee} className="p-4 border-zinc-800 bg-zinc-900/50">
                  <div className="flex items-center justify-between mb-3">
                    <h2 className="font-semibold text-white">{assignee}</h2>
                    <span className="text-zinc-500 text-sm">
                      {list.length} task{list.length !== 1 ? "s" : ""} · {completed} done, {inProgress} in progress, {todo} todo
                    </span>
                  </div>
                  <ul className="space-y-2">
                    {list.slice(0, 5).map((t) => (
                      <li key={t.task_id} className="flex items-center justify-between py-2 border-b border-zinc-800 last:border-0">
                        <Link
                          href={`/dashboard/tasks/${t.task_id}`}
                          className="text-zinc-300 hover:text-white truncate flex-1"
                        >
                          {t.title}
                        </Link>
                        <span className="text-zinc-500 text-xs ml-2">{t.status}</span>
                        <Link href={`/dashboard/tasks/${t.task_id}`}>
                          <Button variant="ghost" size="sm">
                            <ChevronRight className="h-4 w-4" />
                          </Button>
                        </Link>
                      </li>
                    ))}
                  </ul>
                  {list.length > 5 && (
                    <Link
                      href="/dashboard/tasks"
                      className="block text-center text-sm text-cyan-400 hover:text-cyan-300 mt-2"
                    >
                      View all tasks →
                    </Link>
                  )}
                </Card>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
