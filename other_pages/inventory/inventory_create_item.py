import uuid

import pandas as pd
import streamlit as st

from components.inventory_item_form import InventoryItemForm

if "selected_inventory" not in st.session_state.keys():
    st.session_state["selected_inventory"] = None

if "current_inventory_item_sale" not in st.session_state.keys():
    st.session_state["current_inventory_item_for_sale"] = False

if "selected_project" in st.session_state.keys():
    if st.session_state["selected_project"] is not None:
        st.session_state["available_inventories"] = pd.DataFrame(
            st.session_state.api_client.inventories.fetch()
        )

        st.session_state["available_templates"] = pd.DataFrame(
            st.session_state.api_client.transactions.fetch_transaction_templates()
        )

        if "current_inventory_item_form" not in st.session_state.keys():
            st.session_state["current_inventory_item_form"] = InventoryItemForm()
        st.session_state["current_inventory_item_form"].render()
