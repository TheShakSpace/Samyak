"use client"

import { motion, useInView } from "framer-motion"
import { useRef } from "react"

const technologies = [
  { name: "React", category: "Frontend" },
  { name: "FastAPI", category: "Backend" },
  { name: "Supabase", category: "Database" },
  { name: "Next.js", category: "Frontend" },
  { name: "Spline", category: "3D" },
  { name: "TypeScript", category: "Frontend" },
  { name: "PostgreSQL", category: "Database" },
  { name: "Python", category: "Backend" },
]

const logos = technologies.map(tech => ({ name: tech.name }));

export function LogoMarquee() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: "-100px" })

  return (
    <section ref={ref} className="py-16 overflow-hidden">
      <motion.div
        initial={{ opacity: 0 }}
        animate={isInView ? { opacity: 1 } : {}}
        transition={{ duration: 0.6 }}
        className="text-center mb-10"
      >
        <p className="text-sm text-zinc-500 uppercase tracking-wider font-medium">Powered by Enterprise Technologies</p>
      </motion.div>

      <div className="relative">
        {/* Fade masks */}
        <div className="absolute left-0 top-0 bottom-0 w-32 bg-gradient-to-r from-zinc-950 to-transparent z-10 pointer-events-none" />
        <div className="absolute right-0 top-0 bottom-0 w-32 bg-gradient-to-l from-zinc-950 to-transparent z-10 pointer-events-none" />

        {/* Marquee container */}
        <div className="flex animate-marquee">
          {[...technologies, ...technologies].map((tech, index) => (
            <div
              key={index}
              className="flex items-center justify-center min-w-[180px] h-16 mx-8 grayscale opacity-50 hover:grayscale-0 hover:opacity-100 transition-all duration-300 group"
            >
              <div className="flex flex-col items-center gap-1 text-zinc-400 group-hover:text-cyan-400">
                <span className="font-medium text-sm" style={{ fontFamily: "var(--font-mono)" }}>
                  {tech.name}
                </span>
                <span className="text-xs text-zinc-600 group-hover:text-cyan-500/70">{tech.category}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
