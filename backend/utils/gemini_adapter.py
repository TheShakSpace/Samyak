"""
Gemini Adapter - LLM client for Task Management Agent (replaces Llama/Ollama).
Uses Google Gemini API; same interface as orchestrator expects.
"""
import os
from typing import Dict, List, Optional, Any

from config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiResponse:
    """Response object compatible with orchestrator (choices[0].message.content)."""
    def __init__(self, content: str, tool_calls: Optional[List] = None):
        self.choices = [GeminiChoice(content, tool_calls or [])]
        self.model = GEMINI_MODEL


class GeminiChoice:
    def __init__(self, content: str, tool_calls: List):
        self.message = GeminiMessage(content, tool_calls)
        self.finish_reason = "stop"
        self.index = 0


class GeminiMessage:
    def __init__(self, content: str, tool_calls: List):
        self.content = content
        self.role = "assistant"
        self.tool_calls = tool_calls


class GeminiClient:
    """
    Gemini client that mimics the chat.completions interface used by the orchestrator.
    """
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or GEMINI_API_KEY
        self.model = model or GEMINI_MODEL
        self._client = None
        if self.api_key:
            self._init_client()

    def _init_client(self):
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self._client = genai
        except ImportError:
            self._client = None

    def _convert_tools_to_prompt(self, tools: List) -> str:
        """Convert tools list to prompt text for Gemini (tool descriptions)."""
        lines = []
        for tool in tools:
            name = getattr(tool, "__name__", str(tool))
            doc = getattr(tool, "__doc__", "") or "No description"
            lines.append(f"- {name}: {doc.strip().split(chr(10))[0]}")
        return "\n".join(lines)

    @property
    def chat(self):
        """Orchestrator uses client.chat.completions.create (no parens)."""
        return GeminiChatCompletion(self)


class GeminiChatCompletion:
    def __init__(self, client: GeminiClient):
        self.client = client

    @property
    def completions(self):
        """Orchestrator calls client.chat.completions.create(...)"""
        return self

    def create(
        self,
        model: str,
        messages: List[Dict[str, str]],
        tools: Optional[List] = None,
        max_turns: int = 10,
        **kwargs
    ) -> GeminiResponse:
        """Single-turn completion with optional tool descriptions in prompt."""
        if not self.client._client:
            return GeminiResponse(
                "Error: Gemini not configured. Set GEMINI_API_KEY in .env."
            )
        system_content = ""
        user_content = ""
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "system":
                system_content = content
            elif role == "user":
                user_content = content
        prompt = user_content
        if system_content:
            prompt = f"{system_content}\n\nUser request: {user_content}"
        if tools:
            tool_desc = self.client._convert_tools_to_prompt(tools)
            prompt += f"\n\nAvailable tools (use these to fulfill the request):\n{tool_desc}"
        try:
            genai = self.client._client
            gemini_model = genai.GenerativeModel(self.client.model)
            response = gemini_model.generate_content(
                prompt,
                generation_config={"temperature": 0.2, "max_output_tokens": 2048},
            )
            text = response.text if response.text else "No response generated."
            return GeminiResponse(text)
        except Exception as e:
            return GeminiResponse(f"Error from Gemini: {str(e)}")
