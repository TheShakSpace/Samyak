/**
 * AI service – frontend autonomous chatbot using Gemini when NEXT_PUBLIC_GEMINI_API_KEY is set.
 * Otherwise tries backend /api/agent/process.
 */
import { processAgentRequest } from "./tasks-api"

export interface AIMessage {
  id: string
  content: string
  timestamp: string
  source: "user" | "ai"
}

type ChatMessageInput = { role: "user" | "assistant"; parts: string }

/** Extract last user message from conversation */
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

/** Get Gemini API key (available in browser via Next.js inlined env) */
function getGeminiApiKey(): string {
  return (process.env.NEXT_PUBLIC_GEMINI_API_KEY ?? "").trim()
}

/** Call Gemini API directly from frontend – works without backend (autonomous chatbot) */
async function callGeminiFromFrontend(
  request: string,
  history: { role: "user" | "assistant"; parts: string }[] = []
): Promise<string> {
  const apiKey = getGeminiApiKey()
  if (!apiKey) {
    return "Set NEXT_PUBLIC_GEMINI_API_KEY in .env.local (get key from https://aistudio.google.com/apikey), then restart: pnpm dev"
  }
  const model = (process.env.NEXT_PUBLIC_GEMINI_MODEL || "gemini-3-flash-preview").trim()
  const contents: { role: string; parts: { text: string }[] }[] = []
  for (const m of history.slice(-10)) {
    const role = m.role === "assistant" ? "model" : "user"
    const text = typeof m.parts === "string" ? m.parts : (Array.isArray(m.parts) ? m.parts.join(" ") : "")
    if (text.trim()) contents.push({ role, parts: [{ text }] })
  }
  contents.push({ role: "user", parts: [{ text: request }] })
  try {
    const res = await fetch(
      `${GEMINI_API_BASE}/models/${model}:generateContent?key=${encodeURIComponent(apiKey)}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents,
          generationConfig: { maxOutputTokens: 2048, temperature: 0.7 },
        }),
      }
    )
    if (!res.ok) {
      const err = await res.text()
      return `Gemini error (${res.status}): ${err.slice(0, 300)}. Check API key and model (${model}).`
    }
    const data = await res.json()
    const text = data?.candidates?.[0]?.content?.parts?.[0]?.text
    return typeof text === "string" ? text : "No response from Gemini."
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e)
    return `Gemini failed: ${msg}. Check network and NEXT_PUBLIC_GEMINI_API_KEY.`
  }
}

/** Use frontend Gemini when key is set (autonomous chatbot); else try backend */
async function callAgent(request: string, history: ChatMessageInput[] = []): Promise<string> {
  if (getGeminiApiKey()) {
    return callGeminiFromFrontend(request, history)
  }
  try {
    const { response } = await processAgentRequest(request)
    if (response?.trim()) return response
    return "No response from backend. Add NEXT_PUBLIC_GEMINI_API_KEY to .env.local for frontend-only chatbot."
  } catch {
    return "Backend unavailable. Add NEXT_PUBLIC_GEMINI_API_KEY to .env.local (get key from https://aistudio.google.com/apikey), then restart: pnpm dev"
  }
}

export const aiService = {
  /**
   * Chat with task agent. Uses frontend Gemini when NEXT_PUBLIC_GEMINI_API_KEY is set (autonomous chatbot).
   * messages: [{ role, parts }], parts = content string.
   */
  chat: async (
    messages: ChatMessageInput[] | { role: string; parts: string }[],
    _trainingData?: string
  ): Promise<string> => {
    const list = messages as ChatMessageInput[]
    const lastUser = getLastUserMessage(list)
    if (!lastUser.trim()) return "Please send a message."
    return callAgent(lastUser, list)
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
