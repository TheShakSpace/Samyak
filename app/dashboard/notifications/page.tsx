"use client"

import { Bell, CheckCircle2, Info } from "lucide-react"
import { Card } from "@/components/ui/card"

export default function NotificationsPage() {
  return (
    <div className="h-full overflow-auto p-6 md:p-8">
      <div className="max-w-2xl mx-auto space-y-6">
        <h1 className="text-2xl font-bold text-white">Notifications</h1>
        <p className="text-zinc-400 text-sm">
          Task events (created, completed) and agent breakdowns are sent to your configured webhooks (Slack, Discord, Teams). This page is a placeholder for in-app notification history when you add it.
        </p>

        <Card className="p-6 border-zinc-800 bg-zinc-900/50">
          <div className="flex items-start gap-3">
            <Info className="h-5 w-5 text-cyan-400 shrink-0 mt-0.5" />
            <div>
              <h2 className="font-medium text-white mb-1">Webhook notifications</h2>
              <p className="text-zinc-500 text-sm">
                Configure <code className="text-zinc-400">SLACK_WEBHOOK_URL</code>, <code className="text-zinc-400">DISCORD_WEBHOOK_URL</code>, or <code className="text-zinc-400">TEAMS_WEBHOOK_URL</code> in <code className="text-zinc-400">backend/.env</code> to receive task and agent updates in your channels.
              </p>
            </div>
          </div>
        </Card>

        <Card className="p-6 border-zinc-800 bg-zinc-900/50">
          <div className="flex items-center gap-3 text-zinc-500">
            <Bell className="h-8 w-8" />
            <p className="text-sm">No in-app notifications yet. Use the Voice Agent or complete tasks to trigger webhook events.</p>
          </div>
        </Card>
      </div>
    </div>
  )
}
