import os

import pandas as pd
import pyodbc
import sqlalchemy as db
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from tasks.school_and_project_tracker_comments import \
    get_school_project_tracker_comments
from tasks.school_and_project_tracker_tasks import \
    get_school_project_tracker_tasks
from tasks.schools_team_projects import \
    get_schools_team_project_overview_status
from tasks.schools_team_tasks import get_school_team_projects_tasks


def start_connection_with_EK12():
    dotenv_path = os.path.join(os.getcwd(), 'keys', 'credentials.env')
    load_dotenv(dotenv_path)

    user = os.getenv('USERNAME_PORTAL')
    passw = os.getenv('PASSWORD_PORTAL')
    host = os.getenv('SERVER_EK12')
    port = 1433
    database = os.getenv('DATABASE_EK12')

    # Connect to the EK12 Database
    engine = db.create_engine(f'mssql+pyodbc://{user}:{passw}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server')
    connection = engine.connect()
    metadata = db.MetaData()
    Session = sessionmaker(bind=engine)
    session = Session()
    return connection, engine, metadata, session

#Connect to EK12 database
CONNECTION, ENGINE, METADATA, SESSION = start_connection_with_EK12()

# Call all app tasks
school_and_project_tracker_tasks = get_school_project_tracker_tasks()
school_project_tracker_comments = get_school_project_tracker_comments()
schools_team_projects_overview_status = get_schools_team_project_overview_status()
schools_team_projects_tasks = get_school_team_projects_tasks()

# Create a dataframe to store the data
school_and_project_tracker_tasks_df = pd.DataFrame(school_and_project_tracker_tasks)
school_project_tracker_comments_df = pd.DataFrame(school_project_tracker_comments)
schools_team_projects_overview_status_df = pd.DataFrame(schools_team_projects_overview_status)
schools_team_projects_tasks_df = pd.DataFrame(schools_team_projects_tasks)

# Post to the database
school_and_project_tracker_tasks_df.to_sql("SchoolProjectTrackerTasks", ENGINE, schema="asana", if_exists="replace", index=False)
school_project_tracker_comments_df.to_sql("SchoolProjectTrackerComments", ENGINE, schema="asana", if_exists="replace", index=False)
schools_team_projects_overview_status_df.to_sql("SchoolsTeamProjectsOverviewAndStatuses", ENGINE, schema="asana", if_exists="replace", index=False)
schools_team_projects_tasks_df.to_sql("SchoolsTeamProjectsTasks", ENGINE, schema="asana", if_exists="replace", index=False)

