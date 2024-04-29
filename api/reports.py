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

    def fetch_available_transaction_dates(self):
        dates = requests.get(f"{self.url_path}/transactions/available-dates/").json()
        print(f"available transaction dates: {dates}")
        return dates

    def fetch_account_balances_by_date(self, balance_date):
        return requests.get(f"{self.url_path}/account-balance/{balance_date}").json()

    def fetch_all_transactions(self):
        return requests.get(f"{self.url_path}/transactions").json()

    def fetch_all_transactions_for_date(self, ledger_date):
        resp = requests.get(
            f"{self.url_path}/transactions/monthly-transaction-ledger/{ledger_date}"
        ).json()
        print(
            f"fetching transactions for {self.url_path}/transactions/{ledger_date}: {resp}"
        )
        return resp

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

    def fetch_general_ledger(self, balance_date, account):
        return requests.get(
            f"{self.url_path}/reports/general-ledger/{balance_date}/{account}"
        ).json()
