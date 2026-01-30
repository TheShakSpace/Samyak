/**
 * AI service – talks to backend agent (Gemini) for chat, documents, strategy.
 * Fallback: if backend is down, calls Gemini API directly from frontend (NEXT_PUBLIC_GEMINI_API_KEY).
 */
import { processAgentRequest } from "./tasks-api"

export interface AIMessage {
  id: string
  content: string
  timestamp: string
  source: "user" | "ai"
}

type ChatMessageInput = { role: "user" | "assistant"; parts: string }

/** Extract last user message from conversation for agent request */
function getLastUserMessage(messages: ChatMessageInput[]): string {
  for (let i = messages.length - 1; i >= 0; i--) {
    if (messages[i].role === "user") {
      const parts = messages[i].parts
      return typeof parts === "string" ? parts : (Array.isArray(parts) ? parts.join(" ") : "")
    }
  }
  return ""
}

const GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"

/** Fallback: call Gemini API directly from frontend when backend is unavailable */
async function fallbackGemini(request: string): Promise<string> {
  const apiKey = (typeof window !== "undefined" ? process.env.NEXT_PUBLIC_GEMINI_API_KEY : process.env.NEXT_PUBLIC_GEMINI_API_KEY) ?? ""
  if (!apiKey.trim()) {
    return "Backend is unavailable and no frontend Gemini fallback key is set. Add NEXT_PUBLIC_GEMINI_API_KEY to .env.local for fallback, or start the backend (cd backend && python -m uvicorn app:app --port 8000)."
  }
  try {
    const model = process.env.NEXT_PUBLIC_GEMINI_MODEL || "gemini-2.0-flash"
    const res = await fetch(
      `${GEMINI_API_BASE}/models/${model}:generateContent?key=${encodeURIComponent(apiKey)}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{ role: "user", parts: [{ text: request }] }],
          generationConfig: { maxOutputTokens: 2048, temperature: 0.7 },
        }),
      }
    )
    if (!res.ok) {
      const err = await res.text()
      return `Gemini fallback error (${res.status}): ${err.slice(0, 200)}. Check NEXT_PUBLIC_GEMINI_API_KEY.`
    }
    const data = await res.json()
    const text = data?.candidates?.[0]?.content?.parts?.[0]?.text
    return typeof text === "string" ? text : "No response from Gemini."
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e)
    return `Gemini fallback failed: ${msg}. Check network and NEXT_PUBLIC_GEMINI_API_KEY.`
  }
}

/** Call backend agent; on failure or empty response try Gemini fallback if key is set */
async function callAgent(request: string): Promise<string> {
  try {
    const { response } = await processAgentRequest(request)
    if (response?.trim()) return response
    // Empty response – try frontend Gemini fallback
    const fallback = await fallbackGemini(request)
    if (fallback && !fallback.includes("no frontend Gemini fallback key")) return fallback
    return "No response from backend. Add NEXT_PUBLIC_GEMINI_API_KEY to .env.local for fallback."
  } catch {
    const fallback = await fallbackGemini(request)
    if (fallback && !fallback.includes("no frontend Gemini fallback key")) return fallback
    return "Backend unavailable. Start: cd backend && python -m uvicorn app:app --port 8000. Set GEMINI_API_KEY in backend/.env, or add NEXT_PUBLIC_GEMINI_API_KEY to .env.local for frontend fallback."
  }
}

export const aiService = {
  /**
   * Chat with task agent. messages: [{ role, parts }], parts = content string.
   * Returns response text (string).
   */
  chat: async (
    messages: ChatMessageInput[] | { role: string; parts: string }[],
    _trainingData?: string
  ): Promise<string> => {
    const lastUser = getLastUserMessage(messages as ChatMessageInput[])
    if (!lastUser.trim()) return "Please send a message."
    return callAgent(lastUser)
  },

  analyzeUploadedData: async (content: string, filename: string): Promise<string> => {
    const request = `Analyze this uploaded file "${filename}" and summarize key points:\n\n${content.slice(0, 15000)}`
    return callAgent(request)
  },

  generateFinanceDocument: async (documentType: string): Promise<string> => {
    const request = `Generate a professional ${documentType} document (finance/business). Include sections appropriate for that type.`
    return callAgent(request)
  },

  generateFinanceStrategy: async (context: string): Promise<string> => {
    const request = `Generate a finance strategy and recommendations based on this context:\n\n${context}`
    return callAgent(request)
  },
}
