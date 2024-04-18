import requests

from config import URL


class Reports:
    def __init__(self, selected_project):
        self.selected_project_id = selected_project
        self.url_path = f"{URL}/{self.selected_project_id}"

    def fetch_account_balances(self):
        return requests.get(f"{self.url_path}/account-balance").json()

    def fetch_available_balance_dates(self):
        return requests.get(f"{self.url_path}/account-balance/balance-dates").json()

    def fetch_account_balances_by_date(self, balance_date):
        return requests.get(f"{self.url_path}/account-balance/{balance_date}").json()

    def fetch_all_transactions(self):
        return requests.get(f"{self.url_path}/transactions").json()

    def close_month(self, balance_date):
        return requests.put(
            f"{self.url_path}/account-balance/close/{balance_date}"
        ).json()

    def fetch_purchase_journal(self, report_date):
        print(
            f"retrieving purchase journal from {self.url_path}/reports/{report_date}/purchase"
        )
        return requests.get(f"{self.url_path}/reports/{report_date}/purchase").json()

    def fetch_sales_journal(self, report_date):
        print(
            f"retrieving sales journal from {self.url_path}/reports/{report_date}/sales"
        )
        return requests.get(f"{self.url_path}/reports/{report_date}/sales").json()
