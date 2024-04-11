import requests

from config import (
    URL,
    SUPPLIERS_PATH,
    CLIENTS_PATH,
    ADDRESS_PATH,
    BANKING_DETAILS_PATH,
    ORGANISATION_PATH,
)


class ThirdParties:
    def __init__(self, selected_project):
        self.selected_project_id = selected_project
        self.url_path = f"{URL}/{self.selected_project_id}"

    def fetch_suppliers(self):
        print(f"Fetching suppliers from {self.url_path}{SUPPLIERS_PATH}")
        suppliers = requests.get(f"{self.url_path}{SUPPLIERS_PATH}").json()
        print(f"Retrieved {suppliers}")
        return suppliers

    def fetch_clients(self):
        print(f"Fetching clients from {self.url_path}{CLIENTS_PATH}")
        clients = requests.get(f"{self.url_path}{CLIENTS_PATH}").json()
        print(f"Retrieved {clients}")
        return clients

    def fetch_address(self, address_id):
        print(f"fetching address from {self.url_path}{ADDRESS_PATH}/{address_id}")
        return requests.get(f"{self.url_path}{ADDRESS_PATH}/{address_id}").json()

    def fetch_banking_details(self, banking_details_id):
        print(
            f"fetching banking details from {self.url_path}{BANKING_DETAILS_PATH}/{banking_details_id}"
        )
        return requests.get(
            f"{self.url_path}{BANKING_DETAILS_PATH}/{banking_details_id}"
        ).json()

    def fetch_organization_details(self, organization_id):
        return requests.get(
            f"{self.url_path}{ORGANISATION_PATH}/{organization_id}"
        ).json()

    def create_organization(self, organization_data):
        print("Clicked save")
        return requests.post(
            f"{self.url_path}{ORGANISATION_PATH}",
            json=organization_data,
        )
