import type React from "react"
import type { Metadata } from "next"
import { Manrope } from "next/font/google"

import { Analytics } from "@vercel/analytics/next"
import { AuthProvider } from "@/context/auth-context"
import "./globals.css"

const manrope = Manrope({
  subsets: ["latin"],
  variable: "--font-manrope",
})

export const metadata: Metadata = {
  title: "Samyak AI - Enterprise AI Solutions",
  description: "Voice-enabled AI agent with autonomous decision-making. Real-world solutions for enterprise intelligence and automation.",
    generator: 'v0.app'
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${manrope.variable} font-sans antialiased`}>
        <div className="noise-overlay" aria-hidden="true" />
        <AuthProvider>{children}</AuthProvider>
        <Analytics />
      </body>
    </html>
  )
}
