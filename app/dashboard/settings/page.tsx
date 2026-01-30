"use client"

import { Settings, Key, Bell, Database } from "lucide-react"
import { Card } from "@/components/ui/card"
import { useAuth } from "@/context/auth-context"

export default function SettingsPage() {
  const { user } = useAuth()

  return (
    <div className="h-full overflow-auto p-6 md:p-8">
      <div className="max-w-2xl mx-auto space-y-6">
        <h1 className="text-2xl font-bold text-white">Settings</h1>
        <p className="text-zinc-400 text-sm">
          Configuration is done via environment variables. See docs for credentials.
        </p>

        <Card className="p-4 border-zinc-800 bg-zinc-900/50">
          <div className="flex items-center gap-3 mb-3">
            <Key className="h-5 w-5 text-zinc-500" />
            <h2 className="font-medium text-white">API & keys</h2>
          </div>
          <p className="text-zinc-500 text-sm">
            Backend: <code className="text-zinc-400">backend/.env</code> — GEMINI_API_KEY, Firebase, Slack/Discord/Teams webhooks, SMTP. Frontend: <code className="text-zinc-400">.env.local</code> for Firebase web config.
          </p>
          <p className="text-zinc-500 text-sm mt-2">
            See <code className="text-zinc-400">docs/CREDENTIALS_CHECKLIST.md</code> in the project.
          </p>
        </Card>

        <Card className="p-4 border-zinc-800 bg-zinc-900/50">
          <div className="flex items-center gap-3 mb-3">
            <Bell className="h-5 w-5 text-zinc-500" />
            <h2 className="font-medium text-white">Notifications</h2>
          </div>
          <p className="text-zinc-500 text-sm">
            Set SLACK_WEBHOOK_URL, DISCORD_WEBHOOK_URL, or TEAMS_WEBHOOK_URL in backend/.env to receive task and agent notifications.
          </p>
        </Card>

        <Card className="p-4 border-zinc-800 bg-zinc-900/50">
          <div className="flex items-center gap-3 mb-3">
            <Database className="h-5 w-5 text-zinc-500" />
            <h2 className="font-medium text-white">Data</h2>
          </div>
          <p className="text-zinc-500 text-sm">
            Use Firebase Firestore by setting USE_FIREBASE=true and FIREBASE_SERVICE_ACCOUNT_PATH in backend/.env. Otherwise tasks and hours use local JSON/file storage.
          </p>
        </Card>

        {user && (
          <Card className="p-4 border-zinc-800 bg-zinc-900/50">
            <div className="flex items-center gap-3">
              <Settings className="h-5 w-5 text-zinc-500" />
              <div>
                <h2 className="font-medium text-white">Account</h2>
                <p className="text-zinc-500 text-sm mt-1">
                  Logged in as {user.email ?? user.uid ?? "—"}
                </p>
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  )
}
