"use client"

import { useState, useEffect } from "react"
import { BarChart3, Loader2, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { getProductivityReport, type ProductivityReport } from "@/lib/tasks-api"
import { useAuth } from "@/context/auth-context"

export default function AnalyticsPage() {
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

  const statusData = report
    ? [
        { label: "Todo", value: report.status_breakdown.todo, color: "bg-zinc-500" },
        { label: "In progress", value: report.status_breakdown.in_progress, color: "bg-amber-500" },
        { label: "Completed", value: report.status_breakdown.completed, color: "bg-emerald-500" },
      ]
    : []
  const priorityData = report
    ? [
        { label: "High", value: report.priority_breakdown.high, color: "bg-red-500" },
        { label: "Medium", value: report.priority_breakdown.medium, color: "bg-amber-500" },
        { label: "Low", value: report.priority_breakdown.low, color: "bg-zinc-500" },
      ]
    : []
  const maxStatus = Math.max(...statusData.map((d) => d.value), 1)
  const maxPriority = Math.max(...priorityData.map((d) => d.value), 1)

  return (
    <div className="h-full overflow-auto p-6 md:p-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <h1 className="text-2xl font-bold text-white">Analytics</h1>
          <div className="flex gap-2">
            <select
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              className="px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-900 text-white text-sm"
            >
              <option value={7}>7 days</option>
              <option value={14}>14 days</option>
              <option value={30}>30 days</option>
              <option value={90}>90 days</option>
            </select>
            <Button variant="outline" size="sm" onClick={loadReport} className="gap-2">
              <RefreshCw className="h-4 w-4" />
              Refresh
            </Button>
          </div>
        </div>
        <p className="text-zinc-400 text-sm">
          Visual summary of task status and priority from the productivity report.
        </p>

        {report && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="p-4 border-zinc-800 bg-zinc-900/50">
              <h2 className="text-sm font-medium text-zinc-300 mb-4">Status distribution</h2>
              <div className="space-y-3">
                {statusData.map((d) => (
                  <div key={d.label} className="flex items-center gap-3">
                    <span className="text-zinc-400 text-sm w-24">{d.label}</span>
                    <div className="flex-1 h-6 rounded bg-zinc-800 overflow-hidden">
                      <div
                        className={`h-full ${d.color} transition-all`}
                        style={{ width: `${(d.value / maxStatus) * 100}%` }}
                      />
                    </div>
                    <span className="text-white text-sm w-8">{d.value}</span>
                  </div>
                ))}
              </div>
            </Card>
            <Card className="p-4 border-zinc-800 bg-zinc-900/50">
              <h2 className="text-sm font-medium text-zinc-300 mb-4">Priority distribution</h2>
              <div className="space-y-3">
                {priorityData.map((d) => (
                  <div key={d.label} className="flex items-center gap-3">
                    <span className="text-zinc-400 text-sm w-24">{d.label}</span>
                    <div className="flex-1 h-6 rounded bg-zinc-800 overflow-hidden">
                      <div
                        className={`h-full ${d.color} transition-all`}
                        style={{ width: `${(d.value / maxPriority) * 100}%` }}
                      />
                    </div>
                    <span className="text-white text-sm w-8">{d.value}</span>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        )}

        {report && (
          <Card className="p-4 border-zinc-800 bg-zinc-900/50">
            <h2 className="text-sm font-medium text-zinc-300 mb-3">Key metrics</h2>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
              <div>
                <p className="text-zinc-500 text-xs">Completion rate</p>
                <p className="text-2xl font-bold text-emerald-400">{report.completion_rate}%</p>
              </div>
              <div>
                <p className="text-zinc-500 text-xs">Total tasks</p>
                <p className="text-2xl font-bold text-white">{report.total_tasks}</p>
              </div>
              <div>
                <p className="text-zinc-500 text-xs">Hours logged</p>
                <p className="text-2xl font-bold text-violet-400">{report.total_hours_logged ?? 0}</p>
              </div>
              <div>
                <p className="text-zinc-500 text-xs">Avg completion (h)</p>
                <p className="text-2xl font-bold text-cyan-400">{report.average_completion_hours ?? "—"}</p>
              </div>
            </div>
          </Card>
        )}

        {!report && !loading && (
          <p className="text-zinc-500 text-sm">No analytics data. Create tasks and complete them to see charts.</p>
        )}
      </div>
    </div>
  )
}
