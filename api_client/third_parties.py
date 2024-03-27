import requests

from config import (
    URL,
    SUPPLIERS_PATH,
    CLIENTS_PATH,
    ADDRESS_PATH,
    BANKING_DETAILS_PATH,
    ORGANISATION_PATH,
)


def fetch_org_suppliers(id):
    print(f"Fetching suppliers from {URL}/{id}{SUPPLIERS_PATH}")
    suppliers = requests.get(f"{URL}/{id}{SUPPLIERS_PATH}").json()
    print(f"Retrieved {suppliers}")
    return suppliers


def fetch_org_clients(project_id):
    print(f"Fetching clients from {URL}/{project_id}{CLIENTS_PATH}")
    clients = requests.get(f"{URL}/{project_id}{CLIENTS_PATH}").json()
    print(f"Retrieved {clients}")
    return clients


def fetch_agt_clients():
    pass


def fetch_address(project_id, address_id):
    print(f"fetching -> {URL}/{project_id}{ADDRESS_PATH}/{address_id}")
    return requests.get(f"{URL}/{project_id}{ADDRESS_PATH}/{address_id}").json()


def fetch_banking_details(project_id, address_id):
    print(id)
    print(f"fetching -> {URL}/{project_id}{BANKING_DETAILS_PATH}/{address_id}")
    return requests.get(f"{URL}/{project_id}{BANKING_DETAILS_PATH}/{address_id}").json()


def fetch_organization_details(project_id, organization_id):
    return requests.get(
        f"{URL}/{project_id}{ORGANISATION_PATH}/{organization_id}"
    ).json()


def create_organization(project_id, organization_data):
    print("Clicked save")
    print(organization_data)

    return requests.post(
        f"{URL}/{project_id}{ORGANISATION_PATH}", json=organization_data
    )
