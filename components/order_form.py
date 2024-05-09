import uuid

import streamlit as st

from components.invoice_item_form import InvoiceItemForm
from components.order_item_form import OrderItemForm


class OrderForm:
    def __init__(self):
        self.order_items = []
        self.project_id = st.session_state["selected_project"]["id"]
        self.unique_id = uuid.uuid4().hex

        self.invoice_supplier_id = st.session_state.invoice_supplier_id
        self.invoice_clients = st.session_state.invoice_clients
        self.invoice_saved = False
        self.invoice_id = None

        self.serial_number = None
        self.invoice_date = None
        self.due_date = None
        self.currency = None
        self.amount = None
        self.vat_amount = None
        self.issuer_name = None
        self.invoice_client_id = None

    def append_item_to_order(self):
        self.order_items.append(
            OrderItemForm(
                self.project_id,
                self.invoice_date,
                self.invoice_id,
                self.serial_number,
            )
        )
        print(len(self.order_items))
        print(self.order_items)

    def append_service_to_order(self):
        self.order_items.append(
            InvoiceItemForm(
                project_id=st.session_state.selected_project["id"],
                invoice_id=self.invoice_id,
                invoice_date=self.invoice_date.strftime("%Y-%m-%d"),
                invoice_currency=self.currency,
                is_order=True,
            )
        )

    def save(self):
        if all(
            [
                self.serial_number,
                self.invoice_date,
                self.due_date,
                self.invoice_supplier_id,
                self.invoice_client_id,
                self.currency,
                self.amount,
                self.vat_amount,
                self.issuer_name,
            ]
        ):
            self.invoice_saved = True
            self.invoice_id = st.session_state.api_client.invoices.create(
                self.to_dict()
            )
        else:
            st.error("Toate câmpurile sunt obligatorii")

    def to_dict(self):
        invoice_data_dict = {
            "serial_number": self.serial_number,
            "invoice_date": self.invoice_date.strftime("%Y-%m-%d"),
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "supplier_id": int(self.invoice_supplier_id),
            "client_id": int(self.invoice_client_id),
            "currency": self.currency,
            "amount": round(float(self.amount), 2),
            "vat_amount": round(float(self.vat_amount), 2),
            "amount_due": round(float(self.amount), 2)
            + round(float(self.vat_amount), 2),
            "invoice_type": "emisă",
            "payment_type": "încasare",
            "issuer_name": self.issuer_name,
        }

        for key, value in invoice_data_dict.items():
            print(f"{key}: {type(value)}")

        return invoice_data_dict

    def render(self):
        with st.container(border=True):

            c1, c2, c3 = st.columns(3)
            with c1:
                st.write("Furnizor")
                own_org = st.session_state.api_client.projects.get_own_organization()
                with st.container(border=True):
                    st.write(own_org[0]["organization_name"])
                    st.write(own_org[0]["cif"])
                    st.write(own_org[0]["nrc"])

            with c3:
                client = st.selectbox(
                    "Client",
                    self.invoice_clients["organization_name"].tolist(),
                )

                if client:
                    selected_client = self.invoice_clients[
                        self.invoice_clients["organization_name"] == client
                    ]
                    self.invoice_client_id = selected_client["id"].iloc[0]
                    with st.container(border=True):
                        st.write(selected_client.cif.iloc[0])
                        st.write(selected_client.nrc.iloc[0])

            st.header("Detalii factură")

            self.serial_number = st.text_input(
                "Seria", self.serial_number, key=self.unique_id + "serial-number"
            )
            self.invoice_date = st.date_input(
                "Data facturii", key=self.unique_id + "invoice-date"
            )
            self.due_date = st.date_input(
                "Data scadenței", key=self.unique_id + "due-date"
            )

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

            if not self.invoice_saved:
                st.button(
                    "Salvează",
                    key=self.unique_id + "save",
                    on_click=lambda: self.save(),
                )
                st.info("Salvează factura pentru a adăuga articole")

            if self.invoice_saved:
                st.header("Articole comandă")

            if len(self.order_items) > 0:
                for order_item in self.order_items:
                    order_item.render()

            if self.invoice_saved:
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.button("Adaugă articol", on_click=self.append_item_to_order)
                with c2:
                    st.button("Adaugă serviciu", on_click=self.append_service_to_order)
