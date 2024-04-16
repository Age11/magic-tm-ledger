import uuid

import pandas as pd
import streamlit as st

from api_client.transaction import create_transaction_from_template


from components.transaction_card import TransactionCard


class InvoiceItemForm:

    def __init__(self, project_id, invoice_id, invoice_date, invoice_currency):
        self.project_id = project_id
        self.unique_id = uuid.uuid4().hex
        self.invoice_id = invoice_id
        self.invoice_date = invoice_date
        self.currency = invoice_currency

        self.available_templates = st.session_state.available_templates
        self.available_inventories = st.session_state.available_inventories

        self.inventory_id = -self.project_id
        self.selected_template_id = None
        self.saved = False

        self.item_for_sale = False
        self.add_to_inventory = False
        self.use_template = False

        self.name = ""
        self.description = ""
        self.measurement_unit = ""
        self.quantity = 0
        self.acquisition_price = 0
        self.sale_price = 0
        self.vat_rate = 0

        self.item_saved = False
        self.template_saved = False

    def complete(self):
        return all(self.to_dict().values())

    def save(self):
        if self.add_to_inventory:
            if self.complete():

                st.session_state.api_client.inventories.create_inventory_item(
                    self.inventory_id, self.to_dict()
                )
                self.item_saved = True
            else:
                st.info("Toate câmpurile sunt obligatorii pentru a salva un articol.")

        if self.use_template:
            st.session_state.api_client.transactions.create_transaction_from_template(
                transaction_template_id=self.selected_template_id,
                amount=self.quantity * self.acquisition_price,
                date=self.invoice_date,
            )
            self.template_saved = True

    def render(self):
        with st.container(border=True):

            st.write(f"Articol:")

            self.name = st.text_input("Nume", key=self.unique_id + "name")
            self.description = st.text_area(
                "Descriere", key=self.unique_id + "description"
            )

            self.measurement_unit = st.text_input(
                "Unitate de măsură",
                key=self.unique_id + "measurement_unit",
            )
            self.quantity = round(
                st.number_input("Cantitate", key=self.unique_id + "quantity"), 2
            )

            self.acquisition_price = round(
                st.number_input(
                    "Preț de achiziție",
                    key=self.unique_id + "acquisition_price",
                ),
                2,
            )

            self.vat_rate = st.selectbox(
                "Valoare TVA (%)",
                [19, 12, 5, 0],
                index=0,
                key=self.unique_id + "vat_rate",
            )

            self.item_for_sale = st.checkbox(
                "Preț de vânzare", key=self.unique_id + "add_sale_price"
            )

            if self.item_for_sale:
                c1, c2, c3 = st.columns(3)
                with c1:
                    self.sale_price = st.number_input(
                        "Preț de vânzare", key=self.unique_id + "sale_price"
                    )
                with c3:
                    with st.container(border=True):
                        st.write("Marjă:")
                        if self.acquisition_price > 0 and self.sale_price > 0:
                            st.write(
                                f"{round((self.sale_price - self.acquisition_price) / self.acquisition_price * 100, 2)}%"
                            )
                        else:
                            st.write("0%")

            self.add_to_inventory = st.checkbox(
                "Adaugă în inventar", key=self.unique_id + "add_to_inventory"
            )

            if self.add_to_inventory:
                if self.available_inventories.empty:
                    st.write("No available inventories.")
                else:
                    selected_name = st.selectbox(
                        label="Select Inventory",
                        options=self.available_inventories.name.tolist(),
                        index=0,
                        key=f"{self.unique_id} + select_inventory",
                    )
                    self.inventory_id = self.available_inventories[
                        self.available_inventories["name"] == selected_name
                    ]["id"].iloc[0]

            self.use_template = st.checkbox(
                "Selectează tratament contabil predefinit",
                key=self.unique_id + "add_template",
            )

            if self.use_template:
                selected_template = st.selectbox(
                    "Șablon",
                    self.available_templates["name"],
                    key=self.unique_id + "template",
                    index=0,
                )

                self.selected_template_id = (
                    self.available_templates.loc[
                        st.session_state.available_templates["name"]
                        == selected_template,
                        "id",
                    ].iloc[0],
                )[0]

                print(self.selected_template_id)

                main_transaction = self.available_templates.loc[
                    self.available_templates["name"] == selected_template,
                    "main_transaction",
                ].iloc[0]

                self.main_transaction_card = TransactionCard(
                    debit_account=main_transaction["debit_account"],
                    credit_account=main_transaction["credit_account"],
                    details=main_transaction["details"],
                    date=self.invoice_date,
                    currency=main_transaction["currency"],
                    amount=self.acquisition_price * self.quantity,
                )

                self.main_transaction_card.render()

                for transaction in self.available_templates.loc[
                    self.available_templates["name"] == selected_template,
                    "followup_transactions",
                ].iloc[0]:
                    TransactionCard(
                        debit_account=transaction["debit_account"],
                        credit_account=transaction["credit_account"],
                        details=transaction["details"],
                        date=self.invoice_date,
                        currency=main_transaction["currency"],
                        amount=self.acquisition_price * self.quantity,
                        operation=transaction["operation"],
                    ).render()

            if st.button("Salvează articol", key=self.unique_id + "save"):
                self.save()

            if self.item_saved:
                st.info("Articol salvat cu succes.")

            if self.template_saved:
                st.info("Tranzacții înregistrate cu succes.")

    def to_dict(self):

        return {
            "name": self.name,
            "description": self.description,
            "measurement_unit": self.measurement_unit,
            "quantity": self.quantity,
            "acquisition_price": self.acquisition_price,
            "sale_price": self.sale_price,
            "currency": self.currency,
            "vat_rate": self.vat_rate,
            "inventory_id": int(self.inventory_id),
            "invoice_id": int(self.invoice_id),
        }
