import uuid
from datetime import datetime

import pandas as pd
import streamlit as st

from api_client.transaction import create_transaction_from_template
from streamlit_searchbox import st_searchbox

from components.show_transaction_template_form import ShowTemplateForm
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

        self.use_main_template = False
        self.use_second_template = False
        self.main_template = None
        self.second_template = None
        self.available_templates = st.session_state.available_templates
        self.secondary_templates = st.session_state.secondary_templates


        self.name = ""
        self.description = ""
        self.measurement_unit = ""
        self.quantity = None
        self.acquisition_price = 0
        self.vat_rate = 0
        self.units_to_decrease = 0
        self.order_date = order_date.strftime("%Y-%m-%d")
        self.invoice_id = invoice_id

        self.total_sale_price = 0
        self.total_acquisition_cost = 0

        self.saved = False

    def complete(self):
        return all(self.to_dict().values())

    def save(self):
        st.session_state.api_client.inventories.decrease_stock(item_id=self.selected_inventory_items['id'].iloc[0], inventory_id=self.inventory_id, quantity=self.units_to_decrease, invoice_id=self.invoice_id)
        self.saved = True
        if self.use_main_template:
            self.main_template.save()
        if self.use_second_template:
            self.second_template.save()



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
                st.write("Selectează o gestiune")
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
                    placeholder="Caută produs în gestiunea selectată",
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
                    self.total_sale_price = round(self.units_to_decrease * selected_item['sale_price'], 2)
                    self.total_acquisition_cost = round(self.units_to_decrease * selected_item['acquisition_price'], 2)
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

            self.use_main_template = st.checkbox(
                "Selectează tratament contabil predefinit",
                key=self.unique_id + "add_template",
            )

            if self.use_main_template:
                self.main_template = ShowTemplateForm(available_templates=self.available_templates, date=self.order_date, amount=self.total_sale_price)
                self.main_template.render()

            self.use_second_template = st.checkbox(
                "Descărcare din gestiune",
                key=self.unique_id + "add_template2",
            )

            if self.use_second_template:
                self.second_template = ShowTemplateForm(available_templates=self.secondary_templates, date=self.order_date, amount=self.total_acquisition_cost)
                self.second_template.render()


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
