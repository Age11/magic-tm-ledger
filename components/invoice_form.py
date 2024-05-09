import uuid

import streamlit as st
from components.invoice_item_form import InvoiceItemForm


class InflowInvoiceForm:
    def __init__(self, suppliers, client):
        self.unique_id = uuid.uuid4().hex
        self.suppliers = suppliers
        self.invoice_id = None
        self.saved = False
        self.updated = False

        self.serial_number = None
        self.invoice_date = None
        self.due_date = None
        self.supplier = None
        self.client = client
        self.currency = None
        self.amount = None
        self.vat_amount = None
        self.issuer_name = None

        self.inventory_items = []
        self.available_inventories = (st.session_state.available_templates,)
        self.available_templates = st.session_state.available_templates

    def to_dict(self):

        invoice_data_dict = {
            "serial_number": self.serial_number,
            "invoice_date": self.invoice_date.strftime("%Y-%m-%d"),
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "supplier_id": int(self.supplier),
            "client_id": int(self.client),
            "currency": self.currency,
            "amount": round(float(self.amount), 2),
            "invoice_type": "primită",
            "payment_type": "plată",
            "vat_amount": round(float(self.vat_amount), 2),
            "issuer_name": self.issuer_name,
            "amount_due": round(float(self.amount), 2)
            + round(float(self.vat_amount), 2),
        }

        for key, value in invoice_data_dict.items():
            print(f"{key}: {type(value)}")

        return invoice_data_dict

    def save(self):
        if all(
            [
                self.serial_number,
                self.invoice_date,
                self.due_date,
                self.supplier,
                self.client,
                self.currency,
                self.amount,
                self.vat_amount,
                self.issuer_name,
            ]
        ):
            self.saved = True
            self.invoice_id = st.session_state.api_client.invoices.create(
                self.to_dict()
            )
            for item in self.inventory_items:
                item.invoice_id = self.invoice_id
        else:
            st.error("Toate câmpurile sunt obligatorii")

    def update_invoice(self):
        if st.button("Actualizează", key=self.unique_id + "update"):
            if all(
                [
                    self.serial_number,
                    self.invoice_date,
                    self.due_date,
                    self.supplier,
                    self.client,
                    self.currency,
                    self.amount,
                    self.issuer_name,
                ]
            ):
                self.updated = True
                print(self.to_dict())
            else:
                st.error("Toate câmpurile sunt obligatorii")

    def append_inventory_item(self):
        self.inventory_items.append(
            InvoiceItemForm(
                project_id=st.session_state.selected_project["id"],
                invoice_id=self.invoice_id,
                invoice_sn=self.serial_number,
                invoice_date=self.invoice_date.strftime("%Y-%m-%d"),
                invoice_currency=self.currency,
            )
        )

    def render(self):
        with st.container(border=True):
            self.serial_number = st.text_input(
                "Seria", self.serial_number, key=self.unique_id + "serial-number"
            )
            self.invoice_date = st.date_input(
                "Data facturii", key=self.unique_id + "invoice-date"
            )
            self.due_date = st.date_input(
                "Data scadenței", key=self.unique_id + "due-date"
            )
            user_selection = st.selectbox(
                "Furnizor",
                self.suppliers["organization_name"],
                index=0,
            )
            self.supplier = self.suppliers[
                self.suppliers["organization_name"] == user_selection
            ]["id"].iloc[0]

            self.currency = st.selectbox(
                "Moneda", ["RON", "EUR"], key=self.unique_id + "currency"
            )
            self.amount = st.number_input("Suma", key=self.unique_id + "amount")

            self.vat_amount = st.number_input(
                "Suma TVA", key=self.unique_id + "vat-amount"
            )

            self.issuer_name = st.text_input(
                "Nume Emitent", key=self.unique_id + "issuer-name"
            )

            if not self.saved:
                st.button(
                    "Salvează",
                    key=self.unique_id + "save",
                    on_click=lambda: self.save(),
                )

            st.title("Articole factură")

            if self.saved:
                if len(self.inventory_items) > 0:
                    for item_form in self.inventory_items:
                        item_form.render()
                if st.button("Adaugă articol", on_click=self.append_inventory_item):
                    print(self.inventory_items)
            else:
                st.info("Salvează factura pentru a adăuga articole.")
