import uuid

import pandas as pd
import streamlit as st
from api_client.inventory import fetch_inventories
from components.dataframe_with_selection import dataframe_with_selections


class InventorySelectForm:

    def __init__(self, project_id):
        self.project_id = project_id
        self.unique_id = uuid.uuid4().hex
        self.inventory = None
        self.inventory_id = None
        self.available_inventories = None
        self.selected = None

    def render(self):
        self.available_inventories = pd.DataFrame(fetch_inventories(self.project_id))

        if not self.available_inventories.empty:

            user_selection = st.selectbox(
                "Inventare disponibile",
                self.available_inventories["name"].values,
                index=0,
                key=self.unique_id + "inventory",
            )

            self.selected = self.available_inventories[
                self.available_inventories["name"] == user_selection
            ].iloc[0]["id"]

        else:
            st.write("Creează un inventar")
