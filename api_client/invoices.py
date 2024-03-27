import json

import requests

from config import INVOICES_PATH, URL


def fetch_invoices(project_id):
    print(f"retrieving invoices from {URL}/{project_id}{INVOICES_PATH}")
    invoices = requests.get(f"{URL}/{project_id}{INVOICES_PATH}").json()
    print(f"Retrieved {invoices}")
    return invoices


def create_invoice(project_id, invoice_data):
    print(f"Posting invoice: {URL}/{project_id}{INVOICES_PATH}")
    print(invoice_data)
    invoice = requests.post(f"{URL}/{project_id}{INVOICES_PATH}", json=invoice_data)
    print(f"Headers are: {invoice.headers["location"].split("/")[-1]}")
    return invoice.headers["location"].split("/")[-1]


def update_invoice(project_id, invoice_id, invoice_data):
    print(f"Updating invoice with the following data: {invoice_data}")
    print(f"Updating invoice with the following data: {invoice_id}")
    print(f"Updating invoice with the following items: {project_id}")
