import uuid
from datetime import datetime

import streamlit as st

from components.transaction_card import TransactionCard


class InventoryItemForm:

    def __init__(self):

        self.available_inventories = st.session_state.available_inventories
        self.available_templates = st.session_state.available_templates
        self.project_id = st.session_state.selected_project["id"]
        self.unique_id = uuid.uuid4().hex

        self.item_for_sale = False
        self.add_to_inventory = False
        self.saved = False

        self.use_template = None
        self.selected_template_id = None
        self.main_transaction_card = None

        self.name = ""
        self.description = ""
        self.quantity = 0
        self.acquisition_price = 0
        self.vat_rate = 0
        self.inventory_id = -self.project_id
        self.invoice_id = -self.project_id
        self.currency = "RON"
        self.sale_price = 0

    def save(self):
        if all(self.to_dict().values()):
            st.session_state.api_client.inventories.create_inventory_item(
                self.inventory_id, self.to_dict()
            )
            if self.use_template:
                st.session_state.api_client.transactions.create_transaction_from_template(
                    transaction_template_id=self.selected_template_id,
                    amount=self.quantity * self.acquisition_price,
                    date=datetime.now().strftime("%Y-%m-%d"),
                )
            self.saved = True
        else:
            st.info("Toate câmpurile sunt obligatorii pentru a salva un articol.")

    def to_dict(self):

        return {
            "name": self.name,
            "description": self.description,
            "inventory_id": int(self.inventory_id),
            "invoice_id": int(self.invoice_id),
            "measurement_unit": self.measurement_unit,
            "quantity": round(float(self.quantity), 2),
            "acquisition_price": round(float(self.acquisition_price), 2),
            "sale_price": round(float(self.sale_price), 2),
            "vat_rate": int(self.vat_rate),
            "currency": self.currency,
        }

    def render(self):
        with st.container(border=True):
            st.header("Adaugă un articol în gestiune")

            self.name = st.text_input("Nume", key=self.unique_id + "name")
            self.description = st.text_area(
                "Descriere", key=self.unique_id + "description"
            )
            self.quantity = st.number_input(
                "Cantitate", key=self.unique_id + "quantity"
            )

            self.measurement_unit = st.text_input(
                "Unitate de măsură", key=self.unique_id + "measurement_unit"
            )

            self.acquisition_price = st.number_input(
                "Preț de achiziție", key=self.unique_id + "price"
            )

            self.currency = st.selectbox("Monedă", ["RON", "EUR"], index=0)

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
                        st.write("Adaos comercial:")
                        if self.acquisition_price > 0 and self.sale_price > 0:
                            st.write(
                                f"{round((self.sale_price - self.acquisition_price) / self.acquisition_price * 100, 2)}%"
                            )
                        else:
                            st.write("0%")

            self.add_to_inventory = st.checkbox(
                "Adaugă în gestiune", key=self.unique_id + "add_to_inventory"
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
                    date=datetime.now().strftime("%Y-%m-%d"),
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
                        date=datetime.now().strftime("%Y-%m-%d"),
                        currency=main_transaction["currency"],
                        amount=self.acquisition_price * self.quantity,
                        operation=transaction["operation"],
                    ).render()

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Salvează", key=self.unique_id + "save"):
                    self.save()
            with col3:
                st.button(
                    "Resetează", key=self.unique_id + "cancel", on_click=self.__init__
                )
            if self.saved:
                st.info("Articol salvat cu succes!")
