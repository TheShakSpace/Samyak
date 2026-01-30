"use client"

import { useState, useEffect } from "react"
import { Plug, Loader2, CheckCircle2, XCircle, MessageSquare, Calendar, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { getIntegrationsStatus, type IntegrationsStatus } from "@/lib/tasks-api"

export default function IntegrationsPage() {
  const [status, setStatus] = useState<IntegrationsStatus | null>(null)
  const [loading, setLoading] = useState(true)

  const load = async () => {
    setLoading(true)
    try {
      const s = await getIntegrationsStatus()
      setStatus(s)
    } catch {
      setStatus(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  if (loading && !status) {
    return (
      <div className="h-full flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin text-zinc-500" />
      </div>
    )
  }

  const s = status ?? {
    slack_tasks: false,
    slack_agent: false,
    google_oauth: false,
    calendar_sync: false,
  }

  return (
    <div className="h-full overflow-auto p-6 md:p-8">
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="flex items-center justify-between gap-4">
          <h1 className="text-2xl font-bold text-white">Integrations</h1>
          <Button variant="outline" size="sm" onClick={load} className="gap-2">
            <RefreshCw className="h-4 w-4" />
            Refresh
          </Button>
        </div>
        <p className="text-zinc-400 text-sm">
          Slack and Gmail/Calendar are configured in the <strong>backend</strong> via <code className="text-zinc-300">backend/.env</code>. This page shows connection status.
        </p>

        {/* Slack Tasks */}
        <Card className="p-4 border-zinc-800 bg-zinc-900/50">
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-lg bg-[#4A154B]/30">
              <MessageSquare className="h-5 w-5 text-[#E01E5A]" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <h2 className="font-semibold text-white">Slack – Task channel</h2>
                {s.slack_tasks ? (
                  <span className="inline-flex items-center gap-1 text-xs text-emerald-400">
                    <CheckCircle2 className="h-4 w-4" /> Connected
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 text-xs text-zinc-500">
                    <XCircle className="h-4 w-4" /> Not configured
                  </span>
                )}
              </div>
              <p className="text-zinc-500 text-sm mt-1">
                Task created/updated/completed events are posted to <strong>#samayak-project-tasks</strong> (or your configured channel).
              </p>
              <p className="text-zinc-600 text-xs mt-2">
                Configure in <code className="text-zinc-500">backend/.env</code>: <code className="text-zinc-500">WEBHOOK_URL_SLACK_TASKS</code> or <code className="text-zinc-500">WEBHOOK_URL_SLACK</code>
              </p>
            </div>
          </div>
        </Card>

        {/* Slack Agent */}
        <Card className="p-4 border-zinc-800 bg-zinc-900/50">
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-lg bg-[#4A154B]/30">
              <MessageSquare className="h-5 w-5 text-[#E01E5A]" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <h2 className="font-semibold text-white">Slack – Agent channel</h2>
                {s.slack_agent ? (
                  <span className="inline-flex items-center gap-1 text-xs text-emerald-400">
                    <CheckCircle2 className="h-4 w-4" /> Connected
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 text-xs text-zinc-500">
                    <XCircle className="h-4 w-4" /> Not configured
                  </span>
                )}
              </div>
              <p className="text-zinc-500 text-sm mt-1">
                Voice Agent (Gemini) breakdowns are posted to <strong>#samyak</strong> when you use the Agent.
              </p>
              <p className="text-zinc-600 text-xs mt-2">
                Configure in <code className="text-zinc-500">backend/.env</code>: <code className="text-zinc-500">WEBHOOK_URL_SLACK_AGENT</code>
              </p>
            </div>
          </div>
        </Card>

        {/* Google OAuth / Gmail & Calendar */}
        <Card className="p-4 border-zinc-800 bg-zinc-900/50">
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-lg bg-blue-500/20">
              <Calendar className="h-5 w-5 text-blue-400" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <h2 className="font-semibold text-white">Gmail & Google Calendar</h2>
                {s.google_oauth ? (
                  <span className="inline-flex items-center gap-1 text-xs text-emerald-400">
                    <CheckCircle2 className="h-4 w-4" /> OAuth configured
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 text-xs text-zinc-500">
                    <XCircle className="h-4 w-4" /> Not configured
                  </span>
                )}
              </div>
              <p className="text-zinc-500 text-sm mt-1">
                OAuth client is used for Gmail (email) and Google Calendar. <strong>Calendar sync</strong> (e.g. add task due dates to Calendar) is not implemented yet.
              </p>
              <p className="text-zinc-600 text-xs mt-2">
                Configure in <code className="text-zinc-500">backend/.env</code>: <code className="text-zinc-500">GOOGLE_OAUTH_CLIENT_ID</code>, <code className="text-zinc-500">GOOGLE_OAUTH_CLIENT_SECRET</code>. Add authorised redirect URIs in Google Cloud Console (see <code className="text-zinc-500">docs/CREDENTIALS_CHECKLIST.md</code>).
              </p>
              {!s.calendar_sync && (
                <p className="text-amber-500/90 text-xs mt-2">
                  Calendar sync: coming soon. Tasks are not yet auto-added to Google Calendar.
                </p>
              )}
            </div>
          </div>
        </Card>

        <Card className="p-4 border-zinc-800 bg-zinc-900/50">
          <div className="flex items-center gap-3">
            <Plug className="h-5 w-5 text-zinc-500" />
            <div>
              <h2 className="font-medium text-white">Where connections live</h2>
              <p className="text-zinc-500 text-sm mt-1">
                All integrations are driven by <strong>backend</strong> env. When you create a task or use the Voice Agent, the backend sends to Slack if webhooks are set. Gmail/Calendar use the same backend OAuth; frontend only displays status here.
              </p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}
