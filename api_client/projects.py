import config
from config import *
import requests


def fetch_projects(project_id=None):
    return requests.get(f"{URL}{PROJECT_PATH}").json()


def create_project(projcet_data):
    print(projcet_data)
    return requests.post(f"{URL}{PROJECT_PATH}", json=projcet_data)


# TODO link this to the update project screen
def update_project(project_id, project_data):
    return requests.put(f"{URL}{PROJECT_PATH}/{project_id}", json=project_data)


def get_own_organization(project_id):
    print(f"Retrieving data from: {URL}/{project_id}{OWN_ORGANIZATION_PATH}")
    project_organizations = requests.get(
        f"{URL}/{project_id}{OWN_ORGANIZATION_PATH}"
    ).json()
    print(f"Retrieved data {project_organizations}")
    return project_organizations
