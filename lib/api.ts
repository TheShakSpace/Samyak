/**
 * Backend API client (auth, chat, etc.). Same pattern as Gemini - backend holds keys.
 */
const API_BASE =
  typeof window !== "undefined"
    ? (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000")
    : ""

export interface AuthUser {
  uid: string
  email: string | null
  displayName: string
}

export interface AuthResponse {
  token: string
  refreshToken: string
  user: AuthUser
}

function getErrorMessage(data: { detail?: string | string[] }, fallback: string): string {
  const d = data?.detail
  if (typeof d === "string") return d
  if (Array.isArray(d) && d.length) return d[0]
  return fallback
}

export async function login(email: string, password: string): Promise<AuthResponse> {
  const res = await fetch(`${API_BASE}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(getErrorMessage(data, "Login failed"))
  return data
}

export async function signup(
  email: string,
  password: string,
  name: string
): Promise<AuthResponse> {
  const res = await fetch(`${API_BASE}/api/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, name }),
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(getErrorMessage(data, "Signup failed"))
  return data
}

const AUTH_TOKEN_KEY = "samyak_auth_token"
const AUTH_USER_KEY = "samyak_auth_user"

export function getStoredToken(): string | null {
  if (typeof window === "undefined") return null
  return localStorage.getItem(AUTH_TOKEN_KEY)
}

export function getStoredUser(): AuthUser | null {
  if (typeof window === "undefined") return null
  try {
    const raw = localStorage.getItem(AUTH_USER_KEY)
    return raw ? (JSON.parse(raw) as AuthUser) : null
  } catch {
    return null
  }
}

export function setAuthStorage(token: string, user: AuthUser) {
  if (typeof window === "undefined") return
  localStorage.setItem(AUTH_TOKEN_KEY, token)
  localStorage.setItem(AUTH_USER_KEY, JSON.stringify(user))
}

export function clearAuthStorage() {
  if (typeof window === "undefined") return
  localStorage.removeItem(AUTH_TOKEN_KEY)
  localStorage.removeItem(AUTH_USER_KEY)
}
