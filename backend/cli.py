#!/usr/bin/env python3
"""
Command-Line Interface for Task Management & Productivity Agent
"""
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

from tools.task_tools import (
    create_task,
    update_task_status,
    get_tasks_by_priority,
    get_all_tasks,
    calculate_productivity_metrics,
    delete_task,
)
from tools.email_tools import send_task_reminder, send_productivity_summary
from tools.visualization_tools import create_priority_distribution_chart, create_task_completion_chart
from agent.orchestrator import TaskManagementAgent
from utils.validators import validate_config, check_system_health
from utils.logger import setup_logger

logger = setup_logger()

def print_json(data, indent=2):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=indent, default=str))

def cmd_create(args):
    """Create a new task"""
    result = create_task(
        title=args.title,
        description=args.description or "",
        priority=args.priority or "medium",
        deadline=args.deadline,
        assignee=args.assignee or "me",
        tags=args.tags.split(",") if args.tags else []
    )
    if result["status"] == "success":
        print(f"✓ Task created: {result['task_id']}")
        if args.verbose:
            print_json(result["task"])
    else:
        print(f"✗ Error: {result['message']}")
        sys.exit(1)

def cmd_list(args):
    """List tasks"""
    if args.priority:
        result = get_tasks_by_priority(args.priority)
    else:
        result = get_all_tasks(
            status=args.status,
            assignee=args.assignee,
            tag=args.tag
        )
    
    print(f"\nFound {result['count']} task(s):\n")
    
    if args.json:
        print_json(result["tasks"])
    else:
        for task in result["tasks"]:
            deadline_str = task.get("deadline", "No deadline")
            if deadline_str:
                try:
                    deadline_dt = datetime.fromisoformat(deadline_str)
                    deadline_str = deadline_dt.strftime("%Y-%m-%d")
                except:
                    pass
            
            print(f"  [{task['task_id']}] {task['title']}")
            print(f"    Priority: {task['priority']}, Status: {task['status']}")
            print(f"    Deadline: {deadline_str}")
            if task.get('tags'):
                print(f"    Tags: {', '.join(task['tags'])}")
            print()

def cmd_update(args):
    """Update task status"""
    result = update_task_status(args.task_id, args.status)
    if result["status"] == "success":
        print(f"✓ Task {args.task_id} updated to '{args.status}'")
    else:
        print(f"✗ Error: {result['message']}")
        sys.exit(1)

def cmd_delete(args):
    """Delete a task"""
    from tools.task_tools import delete_task
    result = delete_task(args.task_id)
    if result["status"] == "success":
        print(f"✓ Task {args.task_id} deleted")
    else:
        print(f"✗ Error: {result['message']}")
        sys.exit(1)

def cmd_metrics(args):
    """Show productivity metrics"""
    result = calculate_productivity_metrics(
        assignee=args.assignee,
        days=args.days
    )
    
    if args.json:
        print_json(result)
    else:
        print(f"\nProductivity Metrics (Last {result['period_days']} days):")
        print(f"  Total Tasks: {result['total_tasks']}")
        print(f"  Completion Rate: {result['completion_rate']}%")
        print(f"\n  Status Breakdown:")
        print(f"    Completed: {result['status_breakdown']['completed']}")
        print(f"    In Progress: {result['status_breakdown']['in_progress']}")
        print(f"    Todo: {result['status_breakdown']['todo']}")
        print(f"\n  Priority Breakdown:")
        print(f"    High: {result['priority_breakdown']['high']}")
        print(f"    Medium: {result['priority_breakdown']['medium']}")
        print(f"    Low: {result['priority_breakdown']['low']}")
        if result.get('average_completion_hours'):
            print(f"\n  Average Completion Time: {result['average_completion_hours']} hours")

def cmd_chart(args):
    """Generate charts"""
    if args.type == "priority":
        result = create_priority_distribution_chart(args.output)
        print(f"✓ Chart created: {result['chart_path']}")
    elif args.type == "completion":
        result = create_task_completion_chart(days=args.days, output_path=args.output)
        print(f"✓ Chart created: {result['chart_path']}")
    else:
        print(f"✗ Unknown chart type: {args.type}")
        sys.exit(1)

def cmd_email(args):
    """Send email notifications"""
    if args.type == "reminder":
        result = send_task_reminder(args.email, days_ahead=args.days)
        if result.get("email_sent"):
            print(f"✓ Reminder sent to {args.email}")
            print(f"  Tasks: {result['tasks_count']}")
        else:
            print(f"⚠ {result['message']}")
    elif args.type == "summary":
        result = send_productivity_summary(args.email, period_days=args.days)
        if result.get("email_sent"):
            print(f"✓ Summary sent to {args.email}")
        else:
            print(f"⚠ {result['message']}")
    else:
        print(f"✗ Unknown email type: {args.type}")
        sys.exit(1)

def cmd_status(args):
    """Show system status"""
    health = check_system_health()
    config = validate_config()
    
    print("\nSystem Status:")
    print(f"  Health: {health['status'].upper()}")
    
    if health['issues']:
        print("\n  Issues:")
        for issue in health['issues']:
            print(f"    ✗ {issue}")
    
    if health['warnings']:
        print("\n  Warnings:")
        for warning in health['warnings']:
            print(f"    ⚠ {warning}")
    
    print("\n  Configuration:")
    print(f"    Database: {'✓' if config['database_writable'] else '✗'}")
    print(f"    LLM: {'✓' if config['llm_configured'] else '✗'}")
    print(f"    Email: {'✓' if config['email_configured'] else '✗'}")

def cmd_agent(args):
    """Use agent with natural language"""
    agent = TaskManagementAgent()
    response = agent.process_request(args.request)
    
    if response['status'] == 'success':
        print(response.get('response', 'Request processed'))
    elif response['status'] == 'info':
        print(response.get('message', 'Info'))
        if args.verbose:
            print(f"\nAvailable tools: {len(agent.tools)}")
    else:
        print(f"✗ Error: {response.get('message', 'Unknown error')}")
        sys.exit(1)

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Task Management & Productivity Agent CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s create -t "Finish report" -p high -d "2 days"
  %(prog)s list --priority high
  %(prog)s update TASK001 --status completed
  %(prog)s metrics --days 30
  %(prog)s chart --type priority
  %(prog)s agent "Show me all high priority tasks"
        """
    )
    
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    create_parser = subparsers.add_parser('create', help='Create a new task')
    create_parser.add_argument('-t', '--title', required=True, help='Task title')
    create_parser.add_argument('-d', '--description', help='Task description')
    create_parser.add_argument('-p', '--priority', choices=['high', 'medium', 'low'], help='Priority')
    create_parser.add_argument('--deadline', help='Deadline (ISO date or relative like "2 days")')
    create_parser.add_argument('--assignee', help='Assignee')
    create_parser.add_argument('--tags', help='Comma-separated tags')
    create_parser.set_defaults(func=cmd_create)
    
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('--priority', choices=['high', 'medium', 'low'], help='Filter by priority')
    list_parser.add_argument('--status', choices=['todo', 'in_progress', 'completed'], help='Filter by status')
    list_parser.add_argument('--assignee', help='Filter by assignee')
    list_parser.add_argument('--tag', help='Filter by tag')
    list_parser.set_defaults(func=cmd_list)
    
    update_parser = subparsers.add_parser('update', help='Update task status')
    update_parser.add_argument('task_id', help='Task ID')
    update_parser.add_argument('--status', required=True, choices=['todo', 'in_progress', 'completed'], help='New status')
    update_parser.set_defaults(func=cmd_update)
    
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_id', help='Task ID')
    delete_parser.set_defaults(func=cmd_delete)
    
    metrics_parser = subparsers.add_parser('metrics', help='Show productivity metrics')
    metrics_parser.add_argument('--days', type=int, default=30, help='Number of days')
    metrics_parser.add_argument('--assignee', help='Filter by assignee')
    metrics_parser.set_defaults(func=cmd_metrics)
    
    chart_parser = subparsers.add_parser('chart', help='Generate charts')
    chart_parser.add_argument('--type', choices=['priority', 'completion'], required=True, help='Chart type')
    chart_parser.add_argument('--output', help='Output file path')
    chart_parser.add_argument('--days', type=int, default=30, help='Days for completion chart')
    chart_parser.set_defaults(func=cmd_chart)
    
    email_parser = subparsers.add_parser('email', help='Send email notifications')
    email_parser.add_argument('email', help='Recipient email')
    email_parser.add_argument('--type', choices=['reminder', 'summary'], required=True, help='Email type')
    email_parser.add_argument('--days', type=int, default=1, help='Days ahead for reminder or period for summary')
    email_parser.set_defaults(func=cmd_email)
    
    status_parser = subparsers.add_parser('status', help='Show system status')
    status_parser.set_defaults(func=cmd_status)
    
    agent_parser = subparsers.add_parser('agent', help='Use agent with natural language')
    agent_parser.add_argument('request', help='Natural language request')
    agent_parser.set_defaults(func=cmd_agent)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error executing command: {e}", exc_info=True)
        print(f"✗ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

