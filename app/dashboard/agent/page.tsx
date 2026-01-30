"use client"

import dynamic from "next/dynamic"

const AgentRoom = dynamic(() => import("@/components/agent-room"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full flex items-center justify-center bg-zinc-950">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-cyan-400 mx-auto mb-4" />
        <p className="text-zinc-400">Loading Agent Room...</p>
      </div>
    </div>
  ),
})

export default function AgentPage() {
  return (
    <div className="h-full overflow-auto">
      <AgentRoom />
    </div>
  )
}
