"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { CheckSquare, Clock, TrendingUp, MessageCircle, ArrowRight, Loader2 } from "lucide-react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { getTasks, getProductivityReport, type Task, type ProductivityReport } from "@/lib/tasks-api"
import { useAuth } from "@/context/auth-context"

export default function DashboardOverviewPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [report, setReport] = useState<ProductivityReport | null>(null)
  const [loading, setLoading] = useState(true)
  const { user } = useAuth()
  const userId = user?.email ?? user?.uid ?? "me"

  useEffect(() => {
    async function load() {
      setLoading(true)
      try {
        const [tasksRes, prodRes] = await Promise.all([
          getTasks({ assignee: userId }),
          getProductivityReport({ assignee: userId, days: 30 }),
        ])
        setTasks(tasksRes.tasks)
        setReport(prodRes)
      } catch {
        setTasks([])
        setReport(null)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [userId])

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
      <div className="max-w-5xl mx-auto space-y-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Overview</h1>
          <p className="text-zinc-400 text-sm mt-1">
            Your task and productivity summary at a glance.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="p-4 border-zinc-800 bg-zinc-900/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-cyan-500/20">
                <CheckSquare className="h-5 w-5 text-cyan-400" />
              </div>
              <div>
                <p className="text-zinc-500 text-xs">My tasks</p>
                <p className="text-white font-semibold">{tasks.length}</p>
              </div>
            </div>
          </Card>
          <Card className="p-4 border-zinc-800 bg-zinc-900/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-amber-500/20">
                <Clock className="h-5 w-5 text-amber-400" />
              </div>
              <div>
                <p className="text-zinc-500 text-xs">In progress</p>
                <p className="text-white font-semibold">{inProgress.length}</p>
              </div>
            </div>
          </Card>
          <Card className="p-4 border-zinc-800 bg-zinc-900/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-emerald-500/20">
                <TrendingUp className="h-5 w-5 text-emerald-400" />
              </div>
              <div>
                <p className="text-zinc-500 text-xs">Completion rate (30d)</p>
                <p className="text-white font-semibold">{report?.completion_rate ?? 0}%</p>
              </div>
            </div>
          </Card>
          <Card className="p-4 border-zinc-800 bg-zinc-900/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-violet-500/20">
                <Clock className="h-5 w-5 text-violet-400" />
              </div>
              <div>
                <p className="text-zinc-500 text-xs">Hours logged (30d)</p>
                <p className="text-white font-semibold">{report?.total_hours_logged ?? 0}</p>
              </div>
            </div>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card className="p-4 border-zinc-800 bg-zinc-900/50">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-white">Recent tasks</h2>
              <Link href="/dashboard/tasks">
                <Button variant="ghost" size="sm" className="text-zinc-400 hover:text-white gap-1">
                  View all <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
            </div>
            {tasks.length === 0 ? (
              <p className="text-zinc-500 text-sm">No tasks yet.</p>
            ) : (
              <ul className="space-y-2">
                {tasks.slice(0, 5).map((t) => (
                  <li key={t.task_id} className="flex items-center justify-between py-2 border-b border-zinc-800 last:border-0">
                    <span className="text-white text-sm truncate flex-1">{t.title}</span>
                    <span className="text-zinc-500 text-xs ml-2">{t.status}</span>
                  </li>
                ))}
              </ul>
            )}
          </Card>
          <Card className="p-4 border-zinc-800 bg-zinc-900/50">
            <h2 className="text-lg font-semibold text-white mb-4">Quick actions</h2>
            <div className="space-y-2">
              <Link href="/dashboard/agent">
                <Button variant="outline" className="w-full justify-start gap-2 border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-white">
                  <MessageCircle className="h-4 w-4" />
                  Open Voice Agent
                </Button>
              </Link>
              <Link href="/dashboard/tasks">
                <Button variant="outline" className="w-full justify-start gap-2 border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-white">
                  <CheckSquare className="h-4 w-4" />
                  Create task
                </Button>
              </Link>
              <Link href="/dashboard/hours">
                <Button variant="outline" className="w-full justify-start gap-2 border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-white">
                  <Clock className="h-4 w-4" />
                  Log working hours
                </Button>
              </Link>
              <Link href="/dashboard/productivity">
                <Button variant="outline" className="w-full justify-start gap-2 border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-white">
                  <TrendingUp className="h-4 w-4" />
                  Productivity report
                </Button>
              </Link>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}
