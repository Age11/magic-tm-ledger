import requests

from config import (
    URL,
)


class AccountBalance:
    def __init__(self, selected_project):
        self.selected_project_id = selected_project
        self.url_path = f"{URL}/{self.selected_project_id}"

    def fetch_current_profit_or_loss(self):
        print(
            f"Retrieving profit or loss from {self.url_path}/account-balance/profit-or-loss"
        )
        return requests.get(f"{self.url_path}/account-balance/profit-or-loss").json()
