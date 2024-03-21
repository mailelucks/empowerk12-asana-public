import os

from dotenv import load_dotenv
from helpers.asana_helper import get_project_tasks, get_task_stories
from helpers.env_path import define_env_path


def get_school_project_tracker_comments():

    # Load environment variables from .env file
    dotenv_path = define_env_path()
    load_dotenv(dotenv_path) 

    # Setup data pull from School and Project Tracker project
    school_and_project_tracker_gid = os.getenv('SCHOOL_AND_PROJECTS_GID')

    task_opts = {
        'limit': 50, 
        'opt_fields': "name",
    }

     # Get School and Project Tracker task GIDs and Names from the Asana API
    tasks = [{'gid': task['gid'], 'name': task['name']} for task in get_project_tasks(school_and_project_tracker_gid, task_opts)]
    
    # Create an empty array to store the comments and task names
    task_comments = []
    
    # resource_subtype will tell us that the story is a comment and text to get the comment.
    story_opts = {
        'limit': 50, 
        'opt_fields': "resource_subtype,text",
    }

    for task in tasks:

        # Get stories for this task
        stories = get_task_stories(task["gid"], story_opts)
        comments = []

        for story in stories:
            # Per Asana forums, targeting "comment_added" is the best way to get the comments from a task
            if story["resource_subtype"] == "comment_added":
                data = {
                    "task_gid": task["gid"],
                    "task_name": task["name"], 
                    "task_comment": story["text"].replace("\n", " ")
                }
                
                task_comments.append(data)

    return task_comments