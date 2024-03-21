import os
from datetime import datetime

from dotenv import load_dotenv
from helpers.asana_helper import get_project_statuses, get_team_projects
from helpers.env_path import define_env_path


def get_schools_team_project_overview_status():

    # Load environment variables from .env file
    dotenv_path = define_env_path()
    load_dotenv(dotenv_path) 

    # Setup data pull for Schools Team Projects and Statuses
    school_team_gid = os.getenv('SCHOOLS_TEAM_GID')
    
    project_opts = {
        'limit': 50,
        'archived': False,
        'opt_fields': "name,notes",
    }
    status_opts = {
        'limit': 50,
        'opt_fields': "author,author.name,color,created_at,text,title",
    }

     # Save project GIDs and Names from the Asana API
    projects = get_team_projects(school_team_gid, project_opts)

    # Setup empty list to store project statuses
    project_statuses = []

    for project in projects:
        # Get tasks for this project
        statuses = get_project_statuses(project['gid'], status_opts)
        
        # Sanitize project overview
        ProjectOverview = project["notes"].replace("\n", " ") if project["notes"] else 'N/A'

        for status in statuses:
            # Convert the date and text into a more readable format
            CreatedAt = datetime.fromisoformat(status["created_at"].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
            Text = status["text"].replace("\n", " ")

            data = {
                "project_gid": project["gid"],
                "project_name": project["name"],
                "project_overview": ProjectOverview,
                "status_author": status["author"]["name"],
                "status_color": status["color"],
                "created_at": CreatedAt,
                "status_title": status["title"],
                "status_text": Text
            }

            project_statuses.append(data)
    
    return project_statuses