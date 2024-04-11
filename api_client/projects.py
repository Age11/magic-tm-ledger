import config
from config import *
import requests


def fetch_projects():
    return requests.get(f"{URL}{PROJECT_PATH}").json()


def create_project(project_data):
    print(f"creating {project_data}")
    return requests.post(f"{URL}{PROJECT_PATH}", json=project_data)
