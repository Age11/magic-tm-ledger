import requests

from config import URL, OWN_ORGANIZATION_PATH


class Projects:
    def __init__(self, project_id):
        self.project_id = project_id
        self.url_path = f"{URL}/{self.project_id}"

    def update(self, project_data):
        return requests.put(f"{self.url_path}/", json=project_data)

    def get_own_organization(self):
        print(f"Retrieving data from: {self.url_path}{OWN_ORGANIZATION_PATH}")
        project_organizations = requests.get(
            f"{self.url_path}{OWN_ORGANIZATION_PATH}"
        ).json()
        print(f"Retrieved data {project_organizations}")
        return project_organizations
