import requests

from config import URL


class Reports:
    def __init__(self, selected_project):
        self.selected_project_id = selected_project
        self.url_path = f"{URL}/{self.selected_project_id}"

    def fetch_account_balances(self):
        return requests.get(f"{self.url_path}/account-balance").json()

    def fetch_all_transactions(self):
        return requests.get(f"{self.url_path}/transactions").json()
