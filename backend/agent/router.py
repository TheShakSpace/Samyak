from typing import Dict, List, Optional
import re

class RequestRouter:
    """
    Intelligent router that categorizes user requests and determines
    which tools/capabilities should be used.
    """
    
    def __init__(self):
        self.patterns = {
            'task_creation': [
                r'create.*task', r'add.*task', r'new.*task',
                r'make.*task', r'schedule.*task'
            ],
            'task_update': [
                r'update.*task', r'change.*task', r'modify.*task',
                r'mark.*complete', r'complete.*task', r'finish.*task',
                r'start.*task', r'begin.*task'
            ],
            'task_query': [
                r'show.*task', r'list.*task', r'get.*task',
                r'find.*task', r'search.*task', r'query.*task',
                r'what.*task', r'which.*task', r'tasks.*due',
                r'tasks.*priority', r'tasks.*status'
            ],
            'email': [
                r'send.*email', r'email.*reminder', r'remind.*email',
                r'notify.*email', r'summary.*email', r'productivity.*email'
            ],
            'visualization': [
                r'chart', r'graph', r'plot', r'visualize', r'visualization',
                r'show.*chart', r'create.*chart', r'generate.*chart',
                r'productivity.*chart', r'completion.*rate'
            ],
            'metrics': [
                r'metrics', r'statistics', r'stats', r'productivity',
                r'completion.*rate', r'performance', r'analytics'
            ],
            'code_query': [
                r'complex.*query', r'advanced.*filter', r'custom.*query',
                r'generate.*code', r'write.*code.*query'
            ]
        }
    
    def categorize_request(self, request: str) -> List[str]:
        """
        Categorize a user request into one or more categories.
        
        Args:
            request: User's natural language request
        
        Returns:
            List of categories that match the request
        """
        request_lower = request.lower()
        categories = []
        
        for category, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, request_lower):
                    if category not in categories:
                        categories.append(category)
                    break
        
        if not categories:
            categories.append('general')
        
        return categories
    
    def get_recommended_tools(self, categories: List[str]) -> List[str]:
        """
        Get recommended tools based on request categories.
        
        Args:
            categories: List of request categories
        
        Returns:
            List of recommended tool categories
        """
        tool_mapping = {
            'task_creation': 'task_tools',
            'task_update': 'task_tools',
            'task_query': 'task_tools',
            'email': 'email_tools',
            'visualization': 'visualization_tools',
            'metrics': 'task_tools',
            'code_query': 'query_tools',
            'general': 'task_tools'
        }
        
        recommended = []
        for category in categories:
            tool = tool_mapping.get(category)
            if tool and tool not in recommended:
                recommended.append(tool)
        
        return recommended if recommended else ['task_tools']
    
    def route(self, request: str) -> Dict:
        """
        Route a request and return routing information.
        
        Args:
            request: User's natural language request
        
        Returns:
            Dictionary with routing information
        """
        categories = self.categorize_request(request)
        recommended_tools = self.get_recommended_tools(categories)
        
        return {
            'request': request,
            'categories': categories,
            'recommended_tools': recommended_tools,
            'complexity': 'high' if 'code_query' in categories or 'visualization' in categories else 'medium' if len(categories) > 1 else 'low'
        }

