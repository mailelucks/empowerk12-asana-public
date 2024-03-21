import os

from dotenv import load_dotenv
from helpers.asana_helper import get_project_tasks
from helpers.env_path import define_env_path


def get_school_project_tracker_tasks():
    # Load environment variables from .env file if present
    dotenv_path = define_env_path()
    load_dotenv(dotenv_path) 

    # Setup data pull for School and Project Tracker tasks
    school_and_project_gid = os.getenv('SCHOOL_AND_PROJECTS_GID')

    opts = {
        'completed_since': "2012-02-22T02:06:58.158Z", 
        'limit': 50, 
        'archive': False,
        'opt_fields': "name, custom_fields,custom_fields.display_value,custom_fields.name", 
    }

    # Get School and Project Tracker tasks from the Asana API
    tasks = get_project_tasks(school_and_project_gid, opts)

    # Setup empty list to collect returned data
    school_and_project_tracker_tasks = []

    # Iterate through each task and assign the values to its respective variable
    for task in tasks:
        TaskName = task["name"]
        custom_fields = task.get("custom_fields", [])

        for field in custom_fields:
            item_name = field.get("name")
            value = field.get("display_value")

            # Pass in N/A if the value is empty
            if value is None or len(value) == 0:
                value = "N/A"

            if item_name == 'Responsible':
                Responsible = value 
            elif item_name == 'Tech Owner':
                TechOwner = value
            elif item_name == 'Supporting':
                Supporting = value
            elif item_name == 'Status':
                Status = value
            elif item_name == 'Quick Summary':
                QuickSummary = value
                QuickSummarySanitize = QuickSummary.strip()
            elif item_name == 'Type':
                Type = value
            elif item_name == 'ARP':
                ARP = value
            elif item_name == 'ThriveK12':
                ThriveK12 = value
        
        data = {
            "task_gid": task["gid"],
            "task_name": TaskName,
            "responsible": Responsible,
            "tech_owner": TechOwner,
            "supporting": Supporting,
            "status": Status,
            "quick_summary": QuickSummarySanitize,
            "type": Type,
            "ARP": ARP,
            "thrive_k12": ThriveK12
        }

        school_and_project_tracker_tasks.append(data)

    return school_and_project_tracker_tasks