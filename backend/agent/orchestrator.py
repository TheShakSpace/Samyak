from typing import Dict, List, Optional, Any
from config import (
    LLM_MODEL,
    LLM_PROVIDER,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    LLAMA_MODEL_PATH,
    OPENAI_API_KEY,
)
from agent.router import RequestRouter

from tools.task_tools import (
    create_task,
    update_task_status,
    get_tasks_by_priority,
    calculate_productivity_metrics,
    get_all_tasks,
    delete_task,
)
from tools.hours_tools import log_working_hours, get_working_hours

from tools.query_tools import (
    query_tasks_with_code,
)

from tools.email_tools import (
    send_task_reminder,
    send_productivity_summary,
    send_task_completion_notification,
    send_custom_email,
    get_upcoming_tasks_for_reminder,
)

# Visualization tools optional (require matplotlib)
try:
    from tools.visualization_tools import (
        create_productivity_chart,
        create_task_completion_chart,
        create_priority_distribution_chart,
    )
    _VIS_TOOLS = [create_productivity_chart, create_task_completion_chart, create_priority_distribution_chart]
except ImportError:
    _VIS_TOOLS = []


class TaskManagementAgent:
    """
    Main orchestrator for the Task Management & Productivity Agent.
    Coordinates all tools and provides a unified interface.
    """
    
    def __init__(self, model: str = None):
        self.model = model or GEMINI_MODEL or LLM_MODEL
        self.router = RequestRouter()
        self.tools = self._register_all_tools()
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize LLM client - Default Gemini, fallback Llama/OpenAI if configured."""
        if LLM_PROVIDER == "gemini" and GEMINI_API_KEY:
            try:
                from utils.gemini_adapter import GeminiClient
                self.client = GeminiClient()
                print("✓ Using Gemini model")
            except Exception as e:
                print(f"⚠ Gemini initialization failed: {e}")
                self.client = None
            return
        if LLM_PROVIDER == "llama":
            try:
                from utils.llama_adapter import LlamaClient
                self.client = LlamaClient(model_path=LLAMA_MODEL_PATH)
                if self.client.model_path:
                    print("✓ Using Llama model (local)")
                else:
                    print("⚠ Llama model not found.")
                return
            except Exception as e:
                print(f"⚠ Llama failed: {e}")
            self.client = None
            return
        if OPENAI_API_KEY:
            try:
                import aisuite as ai
                self.client = ai.Client()
                print("✓ Using OpenAI via AISuite")
                return
            except ImportError:
                pass
        if GEMINI_API_KEY:
            try:
                from utils.gemini_adapter import GeminiClient
                self.client = GeminiClient()
                print("✓ Using Gemini model")
                return
            except Exception:
                pass
        self.client = None
    
    def _register_all_tools(self) -> List:
        """Register all available tools"""
        tools = [
            create_task,
            update_task_status,
            get_tasks_by_priority,
            calculate_productivity_metrics,
            get_all_tasks,
            delete_task,
            log_working_hours,
            get_working_hours,
            query_tasks_with_code,
            send_task_reminder,
            send_productivity_summary,
            send_task_completion_notification,
            send_custom_email,
            get_upcoming_tasks_for_reminder,
        ]
        tools.extend(_VIS_TOOLS)
        return tools
    
    def process_request(self, request: str, use_llm: bool = True) -> Dict[str, Any]:
        """
        Process a natural language request using the agent.
        
        Args:
            request: User's natural language request
            use_llm: Whether to use LLM for processing (requires Python 3.10+)
        
        Returns:
            Dictionary with response and execution details
        """
        routing = self.router.route(request)
        
        if not use_llm or not self.client:
            return {
                'status': 'info',
                'message': 'LLM not available. Download Llama model or configure OpenAI.',
                'routing': routing,
                'suggestion': 'Download Llama model: ./download_llama.sh or see LLAMA_SETUP.md',
                'available_tools': [tool.__name__ for tool in self.tools],
                'note': 'All tools work directly without LLM - use CLI commands instead'
            }
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a Task Management & Productivity Agent.
You help users manage tasks, track productivity, send reminders, and create visualizations.
Use the available tools to accomplish the user's request.
Be helpful, concise, and action-oriented."""
                    },
                    {
                        "role": "user",
                        "content": request
                    }
                ],
                tools=self.tools,
                max_turns=10
            )
            
            return {
                'status': 'success',
                'response': response.choices[0].message.content,
                'routing': routing,
                'model': self.model,
                'tools_used': len(response.choices[0].message.tool_calls) if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls else 0
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error processing request: {e}',
                'routing': routing,
                'error': str(e)
            }
    
    def get_available_tools(self) -> List[Dict]:
        """Get list of all available tools with descriptions"""
        tools_info = []
        for tool in self.tools:
            tools_info.append({
                'name': tool.__name__,
                'description': tool.__doc__ or 'No description available',
                'module': tool.__module__
            })
        return tools_info
    
    def get_system_status(self) -> Dict:
        """Get system status and capabilities"""
        from db.factory import get_task_manager_factory
        task_manager = get_task_manager_factory()
        all_tasks = task_manager.get_all_tasks()
        
        return {
            'llm_available': self.client is not None,
            'model': self.model if self.client else None,
            'total_tools': len(self.tools),
            'total_tasks': len(all_tasks),
            'capabilities': {
                'task_management': True,
                'code_as_plan': True,
                'email_notifications': True,
                'visualizations': True,
                'reflection': True
            }
        }

