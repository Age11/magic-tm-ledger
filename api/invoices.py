import requests

from config import (
    URL,
    INVENTORY_PATH,
    ITEMS_PATH, INVOICES_PATH,
)


class Invoices:
    def __init__(self, selected_project):
        self.selected_project_id = selected_project
        self.url_path = f"{URL}/{self.selected_project_id}"

    def fetch(self):
        print(f"retrieving invoices from {self.url_path}{INVOICES_PATH}")
        invoices = requests.get(f"{self.url_path}{INVOICES_PATH}").json()
        print(f"Retrieved {invoices}")
        return invoices

    def create(self, invoice_data):
        print(f"Posting invoice: {self.url_path}{INVOICES_PATH}")
        print(invoice_data)
        invoice = requests.post(f"{self.url_path}{INVOICES_PATH}", json=invoice_data)
        print(f"Headers are: {invoice.headers["location"].split("/")[-1]}")
        return invoice.headers["location"].split("/")[-1]

    def update_invoice(self, invoice_id, invoice_data):
        print(f"Updating invoice with the following data: {invoice_data}")
        print(f"Updating invoice with the following data: {invoice_id}")

    def fetch_due_receivable(self):
        print(f"Retrieving receivables from {self.url_path}{INVOICES_PATH}/receivable")
        receivable = requests.get(f"{self.url_path}{INVOICES_PATH}/receivable").json()
        print(f"Retrieved {receivable}")
        return receivable

    def fetch_due_payable(self):
        print(f"Retrieving payables from {self.url_path}{INVOICES_PATH}/payable")
        payable = requests.get(f"{self.url_path}{INVOICES_PATH}/payable").json()
        print(f"Retrieved {payable}")
        return payable

    def solve_payment(self, invoice_id):
        print(f"Solving payment for invoice {invoice_id}")
        requests.put(f"{self.url_path}{INVOICES_PATH}/{invoice_id}/pay")

