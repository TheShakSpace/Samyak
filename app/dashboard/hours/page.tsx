"use client"

import { useState, useEffect } from "react"
import { useSearchParams } from "next/navigation"
import { Clock, Plus, RefreshCw, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { getTasks, logWorkingHours, getWorkingHours, type Task, type WorkingHoursEntry } from "@/lib/tasks-api"
import { useAuth } from "@/context/auth-context"

export default function LogHoursPage() {
  const searchParams = useSearchParams()
  const preselectedTask = searchParams.get("task") ?? ""
  const [tasks, setTasks] = useState<Task[]>([])
  const [entries, setEntries] = useState<WorkingHoursEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [taskId, setTaskId] = useState(preselectedTask)
  const [minutes, setMinutes] = useState("")
  const [date, setDate] = useState(() => new Date().toISOString().slice(0, 10))
  const [notes, setNotes] = useState("")
  const { user } = useAuth()
  const userId = user?.email ?? user?.uid ?? "me"

  const loadData = async () => {
    setLoading(true)
    try {
      const [tasksRes, hoursRes] = await Promise.all([
        getTasks(),
        getWorkingHours({ user_id: userId }),
      ])
      setTasks(tasksRes.tasks)
      setEntries(hoursRes.entries)
    } catch {
      setTasks([])
      setEntries([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [userId])

  useEffect(() => {
    if (preselectedTask) setTaskId(preselectedTask)
  }, [preselectedTask])

  const handleLog = async () => {
    const mins = parseInt(minutes, 10)
    if (!taskId || !mins || mins <= 0) return
    try {
      await logWorkingHours({
        task_id: taskId,
        user_id: userId,
        minutes: mins,
        date: date || undefined,
        notes: notes || undefined,
      })
      setMinutes("")
      setNotes("")
      loadData()
    } catch (e) {
      console.error(e)
    }
  }

  const taskTitle = (id: string) => tasks.find((t) => t.task_id === id)?.title ?? id

  return (
    <div className="h-full overflow-auto p-6 md:p-8">
      <div className="max-w-2xl mx-auto space-y-6">
        <h1 className="text-2xl font-bold text-white">Log working hours</h1>
        <p className="text-zinc-400 text-sm">
          Record time spent on tasks for productivity tracking and reports.
        </p>

        <Card className="p-4 border-zinc-800 bg-zinc-900/50">
          <h2 className="text-sm font-medium text-zinc-300 mb-3">Add entry</h2>
          {loading ? (
            <Loader2 className="h-6 w-6 animate-spin text-zinc-500" />
          ) : (
            <div className="space-y-3">
              <div>
                <label className="text-xs text-zinc-500 block mb-1">Task</label>
                <select
                  value={taskId}
                  onChange={(e) => setTaskId(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-800 text-white text-sm"
                >
                  <option value="">Select task</option>
                  {tasks.map((t) => (
                    <option key={t.task_id} value={t.task_id}>
                      {t.title} ({t.task_id})
                    </option>
                  ))}
                </select>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs text-zinc-500 block mb-1">Minutes</label>
                  <Input
                    type="number"
                    min={1}
                    value={minutes}
                    onChange={(e) => setMinutes(e.target.value)}
                    placeholder="30"
                    className="bg-zinc-800 border-zinc-700 text-white"
                  />
                </div>
                <div>
                  <label className="text-xs text-zinc-500 block mb-1">Date</label>
                  <Input
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                    className="bg-zinc-800 border-zinc-700 text-white"
                  />
                </div>
              </div>
              <div>
                <label className="text-xs text-zinc-500 block mb-1">Notes (optional)</label>
                <Input
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="What did you work on?"
                  className="bg-zinc-800 border-zinc-700 text-white"
                />
              </div>
              <Button onClick={handleLog} className="gap-2" disabled={!taskId || !minutes || parseInt(minutes, 10) <= 0}>
                <Plus className="h-4 w-4" />
                Log hours
              </Button>
            </div>
          )}
        </Card>

        <Card className="p-4 border-zinc-800 bg-zinc-900/50">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-medium text-zinc-300">Recent entries</h2>
            <Button variant="ghost" size="sm" onClick={loadData} className="gap-1">
              <RefreshCw className="h-4 w-4" />
              Refresh
            </Button>
          </div>
          {entries.length === 0 ? (
            <p className="text-zinc-500 text-sm">No hours logged yet.</p>
          ) : (
            <ScrollArea className="h-[280px]">
              <ul className="space-y-2 pr-2">
                {entries.map((e) => (
                  <li key={e.id} className="flex items-center justify-between py-2 border-b border-zinc-800 last:border-0 text-sm">
                    <span className="text-white truncate">{taskTitle(e.task_id)}</span>
                    <span className="text-zinc-400 shrink-0 ml-2">
                      {e.minutes} min · {e.date}
                    </span>
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
