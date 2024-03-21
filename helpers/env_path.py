import os

def define_env_path():
    # Specify the path to the credentials.env file
    dotenv_path = os.path.join(os.getcwd(), 'keys', 'api_keys_ids.env')
    return dotenv_path