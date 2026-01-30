"use client"

import { useState, useEffect } from "react"
import { TrendingUp, Loader2, RefreshCw, Clock, CheckCircle2, Target } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { getProductivityReport, type ProductivityReport } from "@/lib/tasks-api"
import { useAuth } from "@/context/auth-context"

export default function ProductivityPage() {
  const [report, setReport] = useState<ProductivityReport | null>(null)
  const [loading, setLoading] = useState(true)
  const [days, setDays] = useState(30)
  const { user } = useAuth()
  const userId = user?.email ?? user?.uid ?? "me"

  const loadReport = async () => {
    setLoading(true)
    try {
      const r = await getProductivityReport({ assignee: userId, days })
      setReport(r)
    } catch {
      setReport(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadReport()
  }, [userId, days])

  if (loading && !report) {
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
          <h1 className="text-2xl font-bold text-white">Productivity report</h1>
          <div className="flex gap-2 items-center">
            <select
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              className="px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-900 text-white text-sm"
            >
              <option value={7}>Last 7 days</option>
              <option value={14}>Last 14 days</option>
              <option value={30}>Last 30 days</option>
              <option value={90}>Last 90 days</option>
            </select>
            <Button variant="outline" size="sm" onClick={loadReport} className="gap-2">
              <RefreshCw className="h-4 w-4" />
              Refresh
            </Button>
          </div>
        </div>
        <p className="text-zinc-400 text-sm">
          Summary for the last {days} days. Hours come from logged working hours when Firebase is enabled.
        </p>

        {report ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card className="p-4 border-zinc-800 bg-zinc-900/50">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-cyan-500/20">
                  <Target className="h-5 w-5 text-cyan-400" />
                </div>
                <div>
                  <p className="text-zinc-500 text-xs">Total tasks</p>
                  <p className="text-white font-semibold">{report.total_tasks}</p>
                </div>
              </div>
            </Card>
            <Card className="p-4 border-zinc-800 bg-zinc-900/50">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-emerald-500/20">
                  <TrendingUp className="h-5 w-5 text-emerald-400" />
                </div>
                <div>
                  <p className="text-zinc-500 text-xs">Completion rate</p>
                  <p className="text-white font-semibold">{report.completion_rate}%</p>
                </div>
              </div>
            </Card>
            <Card className="p-4 border-zinc-800 bg-zinc-900/50">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-amber-500/20">
                  <CheckCircle2 className="h-5 w-5 text-amber-400" />
                </div>
                <div>
                  <p className="text-zinc-500 text-xs">Completed</p>
                  <p className="text-white font-semibold">{report.status_breakdown.completed}</p>
                </div>
              </div>
            </Card>
            <Card className="p-4 border-zinc-800 bg-zinc-900/50">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-violet-500/20">
                  <Clock className="h-5 w-5 text-violet-400" />
                </div>
                <div>
                  <p className="text-zinc-500 text-xs">Hours logged</p>
                  <p className="text-white font-semibold">{report.total_hours_logged ?? 0}</p>
                </div>
              </div>
            </Card>
          </div>
        ) : null}

        {report && (
          <>
            <Card className="p-4 border-zinc-800 bg-zinc-900/50">
              <h2 className="text-sm font-medium text-zinc-300 mb-3">Status breakdown</h2>
              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <p className="text-zinc-500 text-xs">Todo</p>
                  <p className="text-white font-medium">{report.status_breakdown.todo}</p>
                </div>
                <div>
                  <p className="text-zinc-500 text-xs">In progress</p>
                  <p className="text-white font-medium">{report.status_breakdown.in_progress}</p>
                </div>
                <div>
                  <p className="text-zinc-500 text-xs">Completed</p>
                  <p className="text-white font-medium">{report.status_breakdown.completed}</p>
                </div>
              </div>
            </Card>
            <Card className="p-4 border-zinc-800 bg-zinc-900/50">
              <h2 className="text-sm font-medium text-zinc-300 mb-3">Priority breakdown</h2>
              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <p className="text-zinc-500 text-xs">High</p>
                  <p className="text-white font-medium">{report.priority_breakdown.high}</p>
                </div>
                <div>
                  <p className="text-zinc-500 text-xs">Medium</p>
                  <p className="text-white font-medium">{report.priority_breakdown.medium}</p>
                </div>
                <div>
                  <p className="text-zinc-500 text-xs">Low</p>
                  <p className="text-white font-medium">{report.priority_breakdown.low}</p>
                </div>
              </div>
            </Card>
          </>
        )}

        {!report && !loading && (
          <p className="text-zinc-500 text-sm">No data for this period. Create tasks and log hours to see reports.</p>
        )}
      </div>
    </div>
  )
}
