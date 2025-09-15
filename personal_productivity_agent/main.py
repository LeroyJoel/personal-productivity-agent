#!/usr/bin/env python

import sys
import warnings
from datetime import datetime
from personal_productivity_agent.crew import PersonalProductivityAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs',
        'current_year': str(datetime.now().year)
    }
    
    try:
        PersonalProductivityAgent().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def run_with_inputs(inputs: dict):
    """
    Run the crew with user-provided inputs (from streamlit).
    """
    try:
        # Transform the inputs from Streamlit to match what CrewAI agents expect
        transformed_inputs = {
            # Add current date/time context
            'current_date': datetime.now().strftime("%Y-%m-%d"),
            'current_time': datetime.now().strftime("%H:%M"),
            'current_year': str(datetime.now().year),
            
            # Task management inputs
            'user_tasks': inputs.get('tasks', []),
            'task_priority': inputs.get('priority', 'Medium'),
            
            # Email inputs
            'user_emails': inputs.get('emails', ''),
            
            # Calendar inputs
            'user_events': inputs.get('events', []),
            
            # Report type
            'report_period': inputs.get('report_type', 'Daily').lower(),
            
            # Additional context that might be useful for agents
            'tasks_text': '\n'.join(inputs.get('tasks', [])) if inputs.get('tasks') else '',
            'events_text': '\n'.join(inputs.get('events', [])) if inputs.get('events') else '',
        }
        
        # Filter out empty values to avoid passing empty strings/lists
        filtered_inputs = {k: v for k, v in transformed_inputs.items() if v}
        
        print(f"Transformed inputs: {filtered_inputs}")  # Debug print
        
        result = PersonalProductivityAgent().crew().kickoff(inputs=filtered_inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with inputs: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        PersonalProductivityAgent().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        PersonalProductivityAgent().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        PersonalProductivityAgent().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")