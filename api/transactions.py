import requests

from config import URL, TRANSACTION_TEMPLATES_PATH


class Transactions:
    def __init__(self, selected_project):
        self.selected_project_id = selected_project
        self.url_path = f"{URL}/{self.selected_project_id}"

    def create_transaction(self, transaction_data):
        print(f"Post at {self.url_path}/transactions")
        print(f"Creating transaction with the following data: {transaction_data}")
        return requests.post(f"{self.url_path}/transactions", json=transaction_data)

    def create_transaction_from_template(self, transaction_template_id, amount, date):
        print(
            f"Post at {self.url_path}{TRANSACTION_TEMPLATES_PATH}{transaction_template_id}/use-template"
        )
        return requests.post(
            f"{self.url_path}{TRANSACTION_TEMPLATES_PATH}{transaction_template_id}/use-template",
            json={
                "amount": amount,
                "transaction_date": date,
            },
        )

    def fetch_transaction_templates(self):
        print(
            f"retrieving transaction templates from {self.url_path}{TRANSACTION_TEMPLATES_PATH}"
        )
        transaction_templates = requests.get(
            f"{self.url_path}{TRANSACTION_TEMPLATES_PATH}"
        ).json()
        print(f"Retrieved {transaction_templates}")
        return transaction_templates

    def fetch_transaction_templates_by_type(self, tx_type):
        print(
            f"retrieving inflow transaction templates from {self.url_path}{TRANSACTION_TEMPLATES_PATH}/by-type",
        )
        transaction_templates = requests.get(
            f"{self.url_path}{TRANSACTION_TEMPLATES_PATH}/by-type",
            json={"tx_type": tx_type},
        ).json()
        print(f"Retrieved {transaction_templates}")
        return transaction_templates

    def create_transaction_template(self, transaction_template_data):
        return requests.post(
            f"{self.url_path}{TRANSACTION_TEMPLATES_PATH}",
            json=transaction_template_data,
        )
