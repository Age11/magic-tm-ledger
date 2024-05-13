import requests

from config import PAYMENTS_PATH, URL


class Payments:
    def __init__(self, selected_project):
        self.selected_project_id = selected_project
        self.url_path = f"{URL}/{self.selected_project_id}"

    def fetch_due_receivable_by_date(self, payment_date):
        print(
            f"Retrieving receivables from {self.url_path}{PAYMENTS_PATH}/{payment_date}/receivable"
        )
        receivable = requests.get(
            f"{self.url_path}{PAYMENTS_PATH}/{payment_date}/receivable"
        ).json()
        print(f"Retrieved {receivable}")
        return receivable

    def fetch_due_payable_by_date(self, payment_date):
        print(
            f"Retrieving payables from {self.url_path}{PAYMENTS_PATH}/{payment_date}/payable"
        )
        payable = requests.get(
            f"{self.url_path}{PAYMENTS_PATH}/{payment_date}/payable"
        ).json()
        print(f"Retrieved {payable}")
        return payable

    def fetch_all_payments_by_date(self, payment_date):
        print(
            f"Retrieving payments from {self.url_path}{PAYMENTS_PATH}/{payment_date}/all"
        )
        payments = requests.get(
            f"{self.url_path}{PAYMENTS_PATH}/{payment_date}/all"
        ).json()
        print(f"Retrieved {payments}")
        return payments

    def solve_payment(self, payment_id, amount, installment_type):
        print(f"Solving payment for invoice {payment_id}")
        requests.put(
            f"{self.url_path}{PAYMENTS_PATH}/{payment_id}/pay",
            json={"amount": amount, "installment_type": installment_type},
        )

    def create_payment(self, payment_data):
        print(f"Creating payment with the following data: {payment_data}")
        return requests.post(f"{self.url_path}{PAYMENTS_PATH}", json=payment_data)

    def fetch_available_payment_dates(self):
        return requests.get(f"{self.url_path}{PAYMENTS_PATH}/available-dates").json()

    def fetch_payments_journal_by_date(self, payment_date):
        print(
            f"Retrieving payments from {self.url_path}{PAYMENTS_PATH}/{payment_date}/payment-journal"
        )
        payments = requests.get(
            f"{self.url_path}{PAYMENTS_PATH}/{payment_date}/payment-journal"
        ).json()
        print(f"Retrieved {payments}")
        return payments
