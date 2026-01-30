interface ChatMessage {
  role: "user" | "assistant"
  content: string
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export async function chatWithAI(message: string, history: ChatMessage[] = []): Promise<string> {
  try {
    const response = await fetch(`${API_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
        conversation_history: history.map((msg) => ({
          role: msg.role,
          parts: [{ text: msg.content }],
        })),
      }),
    })

    if (!response.ok) {
      throw new Error("Failed to chat with AI")
    }

    const data = await response.json()
    return data.response
  } catch (error) {
    console.error("[v0] Error chatting with AI:", error)
    throw error
  }
}

export async function analyzeDocument(content: string): Promise<string> {
  try {
    const response = await fetch(`${API_URL}/api/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: content,
      }),
    })

    if (!response.ok) {
      throw new Error("Failed to analyze document")
    }

    const data = await response.json()
    return data.response
  } catch (error) {
    console.error("[v0] Error analyzing document:", error)
    throw error
  }
}

export async function generateStrategy(context: string): Promise<string> {
  try {
    const response = await fetch(`${API_URL}/api/generate-strategy`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: context,
      }),
    })

    if (!response.ok) {
      throw new Error("Failed to generate strategy")
    }

    const data = await response.json()
    return data.response
  } catch (error) {
    console.error("[v0] Error generating strategy:", error)
    throw error
  }
}
