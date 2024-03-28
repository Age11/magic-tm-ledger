import requests

from config import TRANSACTION_TEMPLATES_PATH, URL


def fetch_transaction_templates(project_id):
    print(
        f"retrieving transaction templates from {URL}/{project_id}{TRANSACTION_TEMPLATES_PATH}"
    )
    transaction_templates = requests.get(
        f"{URL}/{project_id}{TRANSACTION_TEMPLATES_PATH}"
    ).json()
    print(f"Retrieved {transaction_templates}")
    return transaction_templates


def create_transaction_template(project_id, transaction_template_data):
    return requests.post(
        f"{URL}/{project_id}{TRANSACTION_TEMPLATES_PATH}",
        json=transaction_template_data,
    )
