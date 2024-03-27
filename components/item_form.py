import streamlit as st

from api_client.inventory import create_inventory_item, update_inventory_item
from components.inventory_select_form import InventorySelectForm


class ItemForm:

    def __init__(self, unique_id, project_id, invoice_id):
        self.unique_id = unique_id
        self.project_id = project_id
        self.invoice_id = invoice_id
        self.inventory_id = None
        self.saved = False
        self.updated = False

        self.exclude_keys = ["unique_id"]
        self.name = ""
        self.description = ""
        self.measurement_unit = ""
        self.quantity = 0
        self.acquisition_price = 0
        self.vat_rate = 0
        self.in_analytical_account = ""
        self.out_analytical_account = ""

    def render(self):
        with st.container(border=True):

            st.write(f"Articol:")

            self.name = st.text_input(
                "Nume", value=self.name, key=self.unique_id + "name"
            )
            self.description = st.text_area(
                "Descriere", value=self.description, key=self.unique_id + "description"
            )

            self.measurement_unit = st.text_input(
                "Unitate de măsură",
                value=self.measurement_unit,
                key=self.unique_id + "measurement_unit",
            )
            self.quantity = st.number_input(
                "Cantitate", value=self.quantity, key=self.unique_id + "quantity"
            )

            add_to_inventory = st.checkbox(
                "Adaugă în inventar", key=self.unique_id + "add_to_inventory"
            )
            if add_to_inventory:
                self.inventory_selector = InventorySelectForm(self.project_id)
                self.inventory_selector.render()
                self.inventory_id = self.inventory_selector.selected
            else:
                self.inventory_id = -self.project_id

            self.acquisition_price = st.number_input(
                "Preț de achiziție",
                value=self.acquisition_price,
                key=self.unique_id + "acquisition_price",
            )

            self.vat_rate = st.number_input(
                "Rată TVA",
                value=self.vat_rate,
                key=self.unique_id + "vat_rate",
            )

            if not self.saved and not self.updated:
                if st.button("Salvează", key=self.unique_id + "save"):
                    print(self.to_dict())
                    create_inventory_item(
                        self.project_id, self.inventory_id, self.to_dict()
                    )
                    self.saved = True
            else:
                if st.button("Actualizează", key=self.unique_id + "update"):
                    print(self.to_dict())
                    update_inventory_item(
                        self.project_id, self.inventory_id, self.to_dict()
                    )
                    self.updated = True
            if self.saved and not self.updated:
                st.success("Articol salvat")
            elif self.updated:
                st.success("Articol actualizat")

    def to_dict(self, exclude_keys=None):
        return {
            "name": self.name,
            "description": self.description,
            "inventory_id": int(self.inventory_id),
            "invoice_id": int(self.invoice_id),
            "measurement_unit": self.measurement_unit,
            "quantity": int(self.quantity),
            "acquisition_price": round(float(self.acquisition_price), 2),
            "vat_rate": int(self.vat_rate),
        }
