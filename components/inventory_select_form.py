import uuid
import pandas as pd
import streamlit as st
from api_client.inventory import fetch_inventories


class InventorySelectForm:

    def __init__(self, project_id):
        self.project_id = project_id
        self.unique_id = uuid.uuid4().hex
        # Use a consistent, unique key for accessing the session state for this form instance
        self.selection_state_key = f"inventory_selection_{self.unique_id}"

    def render(self):
        # Fetch inventories and handle empty case
        inventories_df = pd.DataFrame(fetch_inventories(self.project_id))
        if inventories_df.empty:
            st.write("No available inventories.")
            return

        # Check if there's a previous selection in session state, else default to first item
        if self.selection_state_key not in st.session_state:
            st.session_state[self.selection_state_key] = inventories_df.iloc[0]["id"]

        # Generate options list and map ids for quick access
        options = inventories_df["name"].tolist()
        id_map = inventories_df.set_index("name")["id"].to_dict()

        # Render the selectbox and update session state based on selection
        selected_name = st.selectbox(
            label="Select Inventory",
            options=options,
            index=options.index(
                inventories_df[
                    inventories_df["id"] == st.session_state[self.selection_state_key]
                ]["name"].iloc[0]
            ),
            key=f"select_inventory_{self.unique_id}",
        )
        st.session_state[self.selection_state_key] = id_map[selected_name]

        # Debug: Display current selection from session state
        st.write(f"Selected Inventory ID: {st.session_state[self.selection_state_key]}")
