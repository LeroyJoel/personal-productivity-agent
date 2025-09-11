from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

# Define the PersonalProductivityAgent crew
@CrewBase
class PersonalProductivityAgent():
    """PersonalProductivityAgent crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Load agent and task configurations from YAML files
    @agent
    def task_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['task_manager'], # type: ignore[index]
            verbose=True
        )

    @agent
    def email_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['email_assistant'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def calendar_scheduler(self) -> Agent:
        return Agent(
            config=self.agents_config['calendar_scheduler'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def productivity_reporter(self) -> Agent:
        return Agent(
            config=self.agents_config['productivity_reporter'], # type: ignore[index]
            verbose=True
        )

    # Define tasks for the crew
    @task
    def manage_tasks_task(self) -> Task:
        return Task(
            config=self.tasks_config['manage_tasks_task'], # type: ignore[index]
        )
    
    @task
    def handle_email_task(self) -> Task:
        return Task(
            config=self.tasks_config['handle_email_task'], # type: ignore[index]
        )
    
    @task
    def schedule_calendar_task(self) -> Task:
        return Task(
            config=self.tasks_config['schedule_calendar_task'], # type: ignore[index]
        )

    @task
    def generate_productivity_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_productivity_report_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the PersonalProductivityAgent crew"""
 
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            
        )
