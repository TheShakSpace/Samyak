/**
 * AI service – talks to backend agent (Gemini) for chat, documents, strategy.
 * Uses NEXT_PUBLIC_API_URL and /api/agent/process.
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

/** Call backend agent; show clear error if backend unavailable */
async function callAgent(request: string): Promise<string> {
  try {
    const { response } = await processAgentRequest(request)
    return response || ""
  } catch (err) {
    const msg = err instanceof Error ? err.message : "Backend unavailable"
    return `Could not reach the agent. ${msg}\n\nStart the backend: cd backend && python -m uvicorn app:app --port 8000\nThen set GEMINI_API_KEY in backend/.env for live AI.`
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
