import uuid
from datetime import datetime

import pandas as pd
import streamlit as st

from api_client.transaction import create_transaction_from_template
from streamlit_searchbox import st_searchbox

from components.transaction_card import TransactionCard

class OrderItemForm:

    def __init__(
        self,
        project_id,
        order_date,
        invoice_id,
    ):
        self.project_id = project_id
        self.unique_id = uuid.uuid4().hex

        self.available_inventories = st.session_state.available_inventories

        self.use_template = False
        self.available_templates = st.session_state.available_templates
        self.selected_template_id = None
        self.selected_name = None

        self.name = ""
        self.description = ""
        self.measurement_unit = ""
        self.quantity = None
        self.acquisition_price = 0
        self.vat_rate = 0
        self.units_to_decrease = 0
        self.order_date = order_date.strftime("%Y-%m-%d")
        self.invoice_id = invoice_id

        self.saved = False

    def complete(self):
        return all(self.to_dict().values())

    def save(self):
        #Decrease the stock
        st.session_state.api_client.inventories.decrease_stock(item_id=self.selected_inventory_items['id'].iloc[0], inventory_id=self.inventory_id, quantity=self.units_to_decrease, invoice_id=self.invoice_id)
        self.saved = True
        #Record the transactions
        if self.use_template:
            st.session_state.api_client.transactions.create_transaction_from_template(
                transaction_template_id=self.selected_template_id,
                amount=self.total,
                # TODO
                date=self.order_date,
            )
            self.template_saved = True


    def search_inventory(self, searchterm):
        print(searchterm)
        return self.selected_inventory_items[
            self.selected_inventory_items["name"].str.contains(searchterm)
        ]["name"].tolist()

    def render(self):
        with st.container(border=True):

            if self.available_inventories.empty:
                st.write("No available inventories.")
            else:
                st.write("Selectează un inventar")
                self.selected_name = st.selectbox(
                    label="Select Inventory",
                    options=self.available_inventories.name.tolist(),
                    index=0,
                    key=f"{self.unique_id} + select_inventory",
                )
                self.inventory_id = self.available_inventories[
                    self.available_inventories["name"] == self.selected_name
                    ]["id"].iloc[0]

                self.selected_inventory_items = pd.DataFrame(st.session_state.api_client.inventories.fetch_inventory_items(
                     self.inventory_id
                ))

            if self.selected_inventory_items is not None:
                selected_value = st_searchbox(
                    self.search_inventory,
                    key="searchbox" + self.unique_id,
                    placeholder="Caută produs în inventarul selectat",
                )

            if selected_value:
                selected_item = self.selected_inventory_items[
                    self.selected_inventory_items["name"] == selected_value
                ].iloc[0]
                if self.quantity is None:
                    self.item_quantity = selected_item["quantity"]

                with st.container(border=True):
                    st.write(f"Detalii articol: {selected_item["description"]}")
                    st.write(f"Unitate de măsură: {selected_item["measurement_unit"]}")
                    st.write(f"Preț unitar de achiziție: {selected_item["acquisition_price"]}")
                    st.write(f"Rată TVA: {selected_item["vat_rate"]}")

                col1, col2, col3 = st.columns(3)
                with col2:
                    st.write("Cantitate de scăzut")
                    self.units_to_decrease = st.number_input(
                        "Cantitate", key=self.unique_id + "quantity"
                    )
                    self.total = round(self.units_to_decrease * selected_item['sale_price'], 2)
                with col1:
                    st.write("Stoc rămas")
                    st.write(f"Cantitate: {self.item_quantity - self.units_to_decrease}")
                    st.write(f"Pret total achiziție: {round((self.item_quantity - self.units_to_decrease) * selected_item['acquisition_price'],2)}")
                with col3:
                    with st.container(border=True):
                        st.write("Descărcare")
                        st.write(f"Cantitate: {self.units_to_decrease}")
                        st.write(f"Preț total achiziție: {self.units_to_decrease * selected_item['acquisition_price']}")
                        st.write(f"Preț unitar vânzare: {selected_item['sale_price']}")
                        st.write(f"Preț total vânzare: {round(self.units_to_decrease * selected_item['sale_price'],2)}")
                        st.write(f"Rată TVA: {selected_item['vat_rate']}")
                        st.write(f"Total TVA: {round(self.units_to_decrease * selected_item['acquisition_price'] * selected_item['vat_rate'] / 100, 2)}")
                        st.write(f"Total cu TVA: {round(self.units_to_decrease * selected_item['sale_price'] + self.units_to_decrease * selected_item['sale_price'] * selected_item['vat_rate'] / 100,2)}")



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
                    date=self.order_date,
                    currency=main_transaction["currency"],
                    amount=self.total,
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
                        date=self.order_date,
                        currency=main_transaction["currency"],
                        amount=self.total,
                        operation=transaction["operation"],
                    ).render()
            if not self.saved:
                st.button("Salvează modificare", key=self.unique_id + "save", on_click=self.save)
            else:
                st.write("Cantitate stocuri actualizată")

    def to_dict(self):

        return {
            "name": self.name,
            "description": self.description,
            "measurement_unit": self.measurement_unit,
            "quantity": float(self.quantity),
            "acquisition_price": round(float(self.acquisition_price), 2),
            "vat_rate": int(self.vat_rate),
        }
