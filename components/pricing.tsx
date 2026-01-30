"use client"

import { motion, useInView } from "framer-motion"
import { useRef } from "react"
import { Code2, Database, Zap, Box } from "lucide-react"

const technologies = [
  {
    category: "Frontend",
    icon: Code2,
    items: ["React 19", "Next.js 16", "TypeScript", "Tailwind CSS"],
  },
  {
    category: "Backend",
    icon: Zap,
    items: ["FastAPI", "Python", "Real-time Processing", "Async Workers"],
  },
  {
    category: "Database",
    icon: Database,
    items: ["Supabase", "PostgreSQL", "Vector Search", "Row Level Security"],
  },
  {
    category: "3D & Visualization",
    icon: Box,
    items: ["Spline", "Three.js", "WebGL", "Real-time Rendering"],
  },
]

export function Pricing() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: "-100px" })

  return (
    <section id="pricing" className="py-24 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2
            className="text-3xl sm:text-4xl font-bold text-white mb-4"
            style={{ fontFamily: "var(--font-instrument-sans)" }}
          >
            Technology Stack
          </h2>
          <p className="text-zinc-400 max-w-2xl mx-auto">
            Built with industry-leading technologies for performance, scalability, and reliability.
          </p>
        </motion.div>

        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 40 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
        >
          {technologies.map((tech, index) => {
            const Icon = tech.icon
            return (
              <motion.div
                key={tech.category}
                initial={{ opacity: 0, y: 20 }}
                animate={isInView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.6, delay: 0.3 + index * 0.1 }}
                className="group relative p-6 rounded-2xl bg-zinc-900/50 border border-zinc-800 hover:border-zinc-600 hover:bg-zinc-900 transition-all duration-300 hover:scale-[1.05]"
              >
                <div className="mb-4">
                  <div className="p-3 rounded-lg bg-zinc-800/50 w-fit mb-4 group-hover:bg-zinc-700 transition-colors">
                    <Icon className="w-6 h-6 text-cyan-400" strokeWidth={1.5} />
                  </div>
                  <h3 className="text-lg font-semibold text-white">{tech.category}</h3>
                </div>

                <ul className="space-y-2">
                  {tech.items.map((item) => (
                    <li key={item} className="flex items-center gap-2 text-sm text-zinc-300 group-hover:text-zinc-200 transition-colors">
                      <div className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                      {item}
                    </li>
                  ))}
                </ul>

                <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-cyan-500/0 via-transparent to-cyan-500/0 opacity-0 group-hover:opacity-20 transition-opacity duration-300 pointer-events-none" />
              </motion.div>
            )
          })}
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={isInView ? { opacity: 1 } : {}}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="mt-16 text-center"
        >
          <div className="inline-flex items-center gap-4 p-6 rounded-2xl bg-gradient-to-r from-zinc-900/50 to-zinc-900/30 border border-zinc-800">
            <div className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-sm text-zinc-400">
              All services optimized for <span className="text-white font-medium">production-grade performance</span>
            </span>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
