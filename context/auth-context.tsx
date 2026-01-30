"use client"

import React from "react"
import { createContext, useContext, useEffect, useState } from "react"
import type { AuthUser } from "@/lib/api"
import {
  getStoredUser,
  getStoredToken,
  setAuthStorage,
  clearAuthStorage,
} from "@/lib/api"

interface AuthContextType {
  user: AuthUser | null
  loading: boolean
  logout: () => Promise<void>
  setUserFromAuth: (user: AuthUser, token: string) => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const storedUser = getStoredUser()
    const token = getStoredToken()
    if (storedUser && token) {
      setUser(storedUser)
    }
    setLoading(false)
  }, [])

  const logout = async () => {
    clearAuthStorage()
    setUser(null)
  }

  const setUserFromAuth = (u: AuthUser, token: string) => {
    setAuthStorage(token, u)
    setUser(u)
  }

  return (
    <AuthContext.Provider value={{ user, loading, logout, setUserFromAuth: setUserFromAuth }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
