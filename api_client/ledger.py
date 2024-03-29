import requests

from config import URL


def fetch_account_balances(project_id):
    return requests.get(f"{URL}/{project_id}/account-balance").json()


def fetch_all_transactions(project_id):
    return requests.get(f"{URL}/{project_id}/transactions").json()
