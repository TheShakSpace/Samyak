"""
Llama Adapter - Wrapper to use Llama models instead of OpenAI
"""
import os
import json
from typing import Dict, List, Optional, Any
import subprocess
import tempfile

class LlamaClient:
    """
    Llama client adapter that mimics OpenAI/AISuite interface
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize Llama client
        
        Args:
            model_path: Path to downloaded Llama model (auto-detected if None)
        """
        self.model_path = model_path or self._find_model()
        self.model_loaded = False
        
    def _find_model(self) -> Optional[str]:
        """Find Llama model in default locations"""
        # Check common model paths
        possible_paths = [
            os.path.expanduser("~/.llama/models"),
            os.path.expanduser("~/models"),
            "./models",
            os.path.expanduser("~/.cache/llama"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                # Look for model files
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    if os.path.isdir(item_path):
                        # Check if it's a model directory
                        if any(f.endswith(('.gguf', '.bin', '.safetensors')) for f in os.listdir(item_path)):
                            return item_path
        
        return None
    
    def _call_llama_cli(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Call Llama CLI to generate response
        
        Note: This is a simplified implementation.
        For production, use llama-cpp-python or similar library.
        """
        if not self.model_path:
            raise ValueError("Llama model not found. Please download using: llama model download --source meta --model-id Llama-3.3-70B-Instruct")
        
        # For now, use a placeholder implementation
        # In production, you'd use llama-cpp-python or similar
        try:
            # Try using llama CLI if available
            cmd = [
                "llama", "chat",
                "--model", self.model_path,
                "--prompt", prompt
            ]
            
            if system_prompt:
                cmd.extend(["--system", system_prompt])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                raise RuntimeError(f"Llama CLI error: {result.stderr}")
                
        except FileNotFoundError:
            raise RuntimeError("Llama CLI not found. Please install: pip install llama-stack")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Llama request timed out")
    
    def chat(self):
        """Return chat completion interface"""
        return ChatCompletion(self)
    
    def _convert_tools_to_prompt(self, tools: List) -> str:
        """Convert tools list to prompt format for Llama"""
        tools_desc = []
        for tool in tools:
            if hasattr(tool, '__name__') and hasattr(tool, '__doc__'):
                tools_desc.append(f"- {tool.__name__}: {tool.__doc__ or 'No description'}")
        
        return "\n".join(tools_desc)


class ChatCompletion:
    """Chat completion interface compatible with OpenAI format"""
    
    def __init__(self, client: LlamaClient):
        self.client = client
    
    def create(
        self,
        model: str,
        messages: List[Dict[str, str]],
        tools: Optional[List] = None,
        max_turns: int = 10,
        **kwargs
    ) -> "LlamaResponse":
        """
        Create chat completion
        
        Args:
            model: Model identifier (ignored, uses configured model)
            messages: List of message dicts with 'role' and 'content'
            tools: List of tool functions (optional)
            max_turns: Maximum conversation turns
        
        Returns:
            LlamaResponse object compatible with OpenAI format
        """
        # Extract system and user messages
        system_prompt = None
        user_messages = []
        
        for msg in messages:
            if msg.get("role") == "system":
                system_prompt = msg.get("content", "")
            elif msg.get("role") == "user":
                user_messages.append(msg.get("content", ""))
        
        # Combine user messages
        user_prompt = "\n".join(user_messages)
        
        # Add tools information if provided
        if tools:
            tools_desc = self.client._convert_tools_to_prompt(tools)
            user_prompt += f"\n\nAvailable tools:\n{tools_desc}"
            user_prompt += "\n\nUse these tools to answer the user's request."
        
        # Call Llama
        try:
            response_text = self.client._call_llama_cli(user_prompt, system_prompt)
            
            return LlamaResponse(response_text, tools)
        except Exception as e:
            # Fallback: return error message
            return LlamaResponse(f"Error: {str(e)}", tools)


class LlamaResponse:
    """Response object compatible with OpenAI format"""
    
    def __init__(self, content: str, tools: Optional[List] = None):
        self.choices = [LlamaChoice(content, tools)]
        self.model = "llama-3.3-70b"
        self.usage = {
            "prompt_tokens": len(content.split()),  # Approximation
            "completion_tokens": len(content.split()),
            "total_tokens": len(content.split()) * 2
        }


class LlamaChoice:
    """Choice object compatible with OpenAI format"""
    
    def __init__(self, content: str, tools: Optional[List] = None):
        self.message = LlamaMessage(content, tools)
        self.finish_reason = "stop"
        self.index = 0


class LlamaMessage:
    """Message object compatible with OpenAI format"""
    
    def __init__(self, content: str, tools: Optional[List] = None):
        self.content = content
        self.role = "assistant"
        self.tool_calls = []  # Llama doesn't have native tool calling, but we can parse


# Alternative: Use llama-cpp-python for better integration
def create_llama_client_from_cpp(model_path: str):
    """
    Create Llama client using llama-cpp-python (better integration)
    
    Requires: pip install llama-cpp-python
    """
    try:
        from llama_cpp import Llama
        
        llm = Llama(
            model_path=model_path,
            n_ctx=4096,  # Context window
            n_threads=4,  # CPU threads
            verbose=False
        )
        
        return llm
    except ImportError:
        raise ImportError(
            "llama-cpp-python not installed. "
            "Install with: pip install llama-cpp-python"
        )

