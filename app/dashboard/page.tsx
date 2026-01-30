"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { motion } from "framer-motion"
import { LogOut, Settings, BarChart3, CheckSquare, MessageCircle } from "lucide-react"
import { useAuth } from "@/context/auth-context"
import dynamic from "next/dynamic"
import TasksProductivityView from "@/components/tasks-productivity-view"

const AgentRoom = dynamic(() => import("@/components/agent-room"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-screen flex items-center justify-center bg-zinc-950">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-cyan-400 mx-auto mb-4" />
        <p className="text-zinc-400">Loading Agent Dashboard...</p>
      </div>
    </div>
  ),
})

type View = "agent" | "tasks"

export default function DashboardPage() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [view, setView] = useState<View>("agent")
  const { logout } = useAuth()
  const router = useRouter()

  const handleLogout = async () => {
    await logout()
    router.push("/auth/login")
  }

  return (
    <div className="flex h-screen bg-zinc-950">
      {/* Sidebar */}
      <motion.div
        initial={{ x: sidebarOpen ? 0 : -280 }}
        animate={{ x: sidebarOpen ? 0 : -280 }}
        transition={{ duration: 0.3 }}
        className="w-64 border-r border-zinc-800 bg-zinc-900/50 p-4 flex flex-col"
      >
        <div className="mb-8">
          <h1 className="text-xl font-bold text-white tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>
            SAMYAK AI
          </h1>
          <p className="text-xs text-zinc-500 mt-1">Task & Productivity</p>
        </div>

        <nav className="space-y-2 flex-1">
          <button
            type="button"
            onClick={() => setView("agent")}
            className={`w-full p-3 rounded-lg text-sm flex items-center gap-2 transition-all ${
              view === "agent" ? "bg-zinc-800/50 text-white" : "text-zinc-400 hover:bg-zinc-800 hover:text-white"
            }`}
          >
            <MessageCircle className="w-4 h-4" />
            Voice Agent
          </button>
          <button
            type="button"
            onClick={() => setView("tasks")}
            className={`w-full p-3 rounded-lg text-sm flex items-center gap-2 transition-all ${
              view === "tasks" ? "bg-zinc-800/50 text-white" : "text-zinc-400 hover:bg-zinc-800 hover:text-white"
            }`}
          >
            <CheckSquare className="w-4 h-4" />
            Tasks & Hours
          </button>
          <button className="w-full p-3 rounded-lg text-zinc-400 hover:bg-zinc-800 hover:text-white transition-all text-sm flex items-center gap-2">
            <BarChart3 className="w-4 h-4" />
            Analytics
          </button>
          <button className="w-full p-3 rounded-lg text-zinc-400 hover:bg-zinc-800 hover:text-white transition-all text-sm flex items-center gap-2">
            <Settings className="w-4 h-4" />
            Settings
          </button>
        </nav>

        <button
          type="button"
          onClick={handleLogout}
          className="w-full p-3 rounded-lg bg-zinc-800/30 text-zinc-400 hover:bg-red-900/20 hover:text-red-400 transition-all text-sm flex items-center gap-2"
        >
          <LogOut className="w-4 h-4" />
          Logout
        </button>
      </motion.div>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden">
        {view === "agent" && <AgentRoom />}
        {view === "tasks" && <TasksProductivityView />}
      </div>
    </div>
  )
}
