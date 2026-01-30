"use client"

import dynamic from "next/dynamic"
import { motion } from "framer-motion"
import { ArrowRight } from "lucide-react"
import { Button } from "@/components/ui/button"

const Spline = dynamic(() => import("@splinetool/react-spline").then((mod) => mod.default), {
  loading: () => <div className="w-full h-screen bg-zinc-950" />,
  ssr: false,
})

export function SplineHero() {
  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden bg-zinc-950">
      {/* Spline Scene */}
      <div className="absolute inset-0 w-full h-full">
        <Spline scene="https://prod.spline.design/8N5uL9dxEB0Sxr9a/scene.splinecode" />
      </div>

      {/* Watermark Cover & Right Corner Content */}
      <div className="absolute inset-0 pointer-events-none">
        {/* Hide watermark - cover bottom right corner */}
        <div className="absolute bottom-0 right-0 w-32 h-16 bg-gradient-to-l from-zinc-950 to-transparent pointer-events-none" />

        {/* Right Corner Content */}
        <div className="absolute bottom-8 right-8 pointer-events-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex flex-col items-end gap-4"
          >
            <div className="text-right">
              <p className="text-sm text-zinc-400 mb-1">Remote Team Productivity</p>
              <div className="space-y-1">
                <p className="text-2xl font-bold text-white">Task & Management</p>
                <p className="text-xs text-zinc-500">AI-Powered • Assign • Track • Report</p>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Content Overlay - Buttons Only */}
      <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="z-10 pointer-events-auto"
        >
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a href="/dashboard">
              <Button
                size="lg"
                className="shimmer-btn bg-white text-zinc-950 hover:bg-zinc-200 rounded-full px-8 h-12 text-base font-medium shadow-lg shadow-white/10"
              >
                Get Started
                <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            </a>
            <Button
              variant="outline"
              size="lg"
              className="rounded-full px-8 h-12 text-base font-medium border-zinc-800 text-zinc-300 hover:bg-zinc-900 hover:text-white hover:border-zinc-700 bg-zinc-900/40 backdrop-blur-sm"
            >
              View Demo
            </Button>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
