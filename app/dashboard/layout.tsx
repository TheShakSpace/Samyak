"use client"

import { useRouter, usePathname } from "next/navigation"
import Link from "next/link"
import { motion } from "framer-motion"
import {
  LogOut,
  Settings,
  BarChart3,
  CheckSquare,
  MessageCircle,
  LayoutDashboard,
  Clock,
  TrendingUp,
  Users,
  UserCheck,
  Bell,
  Plug,
} from "lucide-react"
import { useAuth } from "@/context/auth-context"
import { cn } from "@/lib/utils"

const nav = [
  { href: "/dashboard", label: "Overview", icon: LayoutDashboard },
  { href: "/dashboard/agent", label: "Voice Agent", icon: MessageCircle },
  { href: "/dashboard/tasks", label: "Tasks", icon: CheckSquare },
  { href: "/dashboard/hours", label: "Log Hours", icon: Clock },
  { href: "/dashboard/productivity", label: "Productivity", icon: TrendingUp },
  { href: "/dashboard/analytics", label: "Analytics", icon: BarChart3 },
  { href: "/dashboard/team", label: "Team", icon: Users },
  { href: "/dashboard/my-work", label: "My Work", icon: UserCheck },
  { href: "/dashboard/notifications", label: "Notifications", icon: Bell },
  { href: "/dashboard/integrations", label: "Integrations", icon: Plug },
  { href: "/dashboard/settings", label: "Settings", icon: Settings },
]

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()
  const { logout } = useAuth()
  const router = useRouter()

  const handleLogout = async () => {
    await logout()
    router.push("/auth/login")
  }

  return (
    <div className="flex h-screen bg-zinc-950">
      <motion.aside
        initial={false}
        className="w-64 border-r border-zinc-800 bg-zinc-900/50 p-4 flex flex-col shrink-0"
      >
        <Link href="/dashboard" className="mb-8 block">
          <h1 className="text-xl font-bold text-white tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>
            SAMYAK
          </h1>
          <p className="text-xs text-zinc-500 mt-1">Task & Productivity</p>
        </Link>

        <nav className="space-y-1 flex-1 overflow-y-auto">
          {nav.map(({ href, label, icon: Icon }) => {
            const isActive = pathname === href || (href !== "/dashboard" && pathname.startsWith(href))
            return (
              <Link
                key={href}
                href={href}
                className={cn(
                  "w-full p-3 rounded-lg text-sm flex items-center gap-2 transition-all",
                  isActive ? "bg-zinc-800/50 text-white" : "text-zinc-400 hover:bg-zinc-800 hover:text-white"
                )}
              >
                <Icon className="w-4 h-4 shrink-0" />
                {label}
              </Link>
            )
          })}
        </nav>

        <button
          type="button"
          onClick={handleLogout}
          className="w-full p-3 rounded-lg bg-zinc-800/30 text-zinc-400 hover:bg-red-900/20 hover:text-red-400 transition-all text-sm flex items-center gap-2"
        >
          <LogOut className="w-4 h-4" />
          Logout
        </button>
      </motion.aside>

      <main className="flex-1 overflow-hidden flex flex-col">
        {children}
      </main>
    </div>
  )
}
