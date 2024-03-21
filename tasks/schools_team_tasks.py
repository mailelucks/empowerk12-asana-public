import os
from datetime import datetime

from dotenv import load_dotenv
from helpers.asana_helper import (get_project_tasks,
                                  get_team_projects)
from helpers.env_path import define_env_path


def get_school_team_projects_tasks():

    # Load environment variables from .env file
    dotenv_path = define_env_path()
    load_dotenv(dotenv_path) 

    # # Setup data pull for Schools team projects and tasks
    school_team_gid = os.getenv('SCHOOLS_TEAM_GID')

    project_opts = {
        'limit': 50,
        'archived': False,
        'opt_fields': "name",
    }

     # Save project GIDs and Names from the Asana API
    projects = [{'gid': project['gid'], 'name': project['name']} for project in get_team_projects(school_team_gid, project_opts)]

    # Iterate through projects to get their tasks and construct table with requested data
    task_opts = {
        'completed_since': "2012-02-22T02:06:58.158Z", 
        'limit': 50, 
        'opt_fields': "assignee,assignee.name,completed,completed_at,due_on,name,memberships,memberships.section,memberships.section.name",
    }
    
    # Create an empty array to store projects and their tasks
    projects_tasks = []

    for project in projects:
        
        # Get tasks for this project
        tasks = get_project_tasks(project["gid"], task_opts)

        for task in tasks:
            # Format time to human readable format
            CompletedAt = datetime.fromisoformat(task["completed_at"].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S') if task["completed_at"] is not None else "N/A"

            # Get the section name for the task
            for membership in task["memberships"]:
                if membership["section"] is not None:
                    TaskSection = membership["section"]["name"]
                    break

            data = {
                "task_gid": task["gid"],
                "task_section": TaskSection,
                "task_name": task["name"],
                "assignee": task["assignee"]["name"] if task["assignee"] is not None else "N/A",
                "completed": "Completed" if task["completed"] != False else "Incomplete",
                "completed_at": CompletedAt,
                "due_on": task["due_on"] if task["due_on"] is not None else "N/A",
                "project_gid": project["gid"],
                "project_name": project["name"],
            }

            projects_tasks.append(data)
        
    return projects_tasks
    