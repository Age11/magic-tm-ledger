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

    def fetch_incoming_by_date(self, invoice_date):
        print(f"retrieving invoices from {self.url_path}{INVOICES_PATH}/{invoice_date}/incoming")
        invoices = requests.get(f"{self.url_path}{INVOICES_PATH}/{invoice_date}/incoming").json()
        print(f"Retrieved {invoices}")
        return invoices

    def fetch_outgoing_by_date(self, invoice_date):
        print(f"retrieving invoices from {self.url_path}{INVOICES_PATH}/{invoice_date}/outgoing")
        invoices = requests.get(f"{self.url_path}{INVOICES_PATH}/{invoice_date}/outgoing").json()
        print(f"Retrieved {invoices}")
        return invoices

    def fetch_all_by_date(self, invoice_date):
        print(f"retrieving invoices from {self.url_path}{INVOICES_PATH}/{invoice_date}/all")
        invoices = requests.get(f"{self.url_path}{INVOICES_PATH}/{invoice_date}/all").json()
        print(f"Retrieved {invoices}")
        return invoices

    def fetch_available_dates(self):
        return requests.get(f"{self.url_path}{INVOICES_PATH}/invoice-dates").json()

    def create(self, invoice_data):
        print(f"Posting invoice: {self.url_path}{INVOICES_PATH}")
        print(invoice_data)
        invoice = requests.post(f"{self.url_path}{INVOICES_PATH}", json=invoice_data)
        print(f"Headers are: {invoice.headers["location"].split("/")[-1]}")
        return invoice.headers["location"].split("/")[-1]

    def update_invoice(self, invoice_id, invoice_data):
        print(f"Updating invoice with the following data: {invoice_data}")
        print(f"Updating invoice with the following data: {invoice_id}")



