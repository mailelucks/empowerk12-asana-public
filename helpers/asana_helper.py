import os

import asana
from asana.rest import ApiException
from dotenv import load_dotenv
from helpers.env_path import define_env_path


def connect_asana():
    # Load environment variables from .env file if present
    dotenv_path = define_env_path()
    load_dotenv(dotenv_path) 

    # Connect to the Asana API
    configuration = asana.Configuration()
    configuration.access_token = os.getenv('ASANA_KEY')
    api_client = asana.ApiClient(configuration)

    return api_client

def get_project_tasks(project_gid, opts):

    # Connect to the Asana API
    api_client = connect_asana()

    # Create Task instance of the API class
    api_instance = asana.TasksApi(api_client)

    try:
        # Get tasks based on Project GID from the Asana API
        tasks = api_instance.get_tasks_for_project(project_gid, opts)

        return tasks

    except ApiException as e:
        print("Exception when calling TasksApi->get_tasks_for_project: %s\n" % e)

       
def get_task_stories(task_gid, opts):

    # Connect to the Asana API
    api_client = connect_asana()

    # Create a Story API instances of the API class
    stories_api_instance = asana.StoriesApi(api_client)

    try:
        
        # Get stories based on Task GID from the Asana API
        stories = stories_api_instance.get_stories_for_task(task_gid, opts)

        return stories

    except ApiException as e:
        print("Exception when calling TasksApi->get_tasks_for_project: %s\n" % e)

def get_team_projects(team_gid, opts):

    # Connect to the Asana API
    api_client = connect_asana()

    # Create a Story API instances of the API class
    projects_api_instance = asana.ProjectsApi(api_client)

    try:
        
        teams_api_response = projects_api_instance.get_projects_for_team(team_gid, opts)
        
        return teams_api_response

    except ApiException as e:
        print("Exception when calling TasksApi->get_tasks_for_project: %s\n" % e)

def get_project_statuses(project_gid, opts):

    # Connect to the Asana API
    api_client = connect_asana()

    # Create a Story API instances of the API class
    projects_api_instance = asana.ProjectStatusesApi(api_client)

    try:
        
        project_statuses_response = projects_api_instance.get_project_statuses_for_project(project_gid, opts)
        
        return project_statuses_response

    except ApiException as e:
        print("Exception when calling TasksApi->get_tasks_for_project: %s\n" % e)