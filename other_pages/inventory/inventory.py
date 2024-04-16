import pandas as pd
import streamlit as st
from components.dataframe_with_selection import dataframe_with_selections
import api_client.inventory as inventory_api

st.title("Inventar")

if "selected_project" in st.session_state.keys():
    if not st.session_state["selected_project"] is None:
        selected_project_id = st.session_state["selected_project"]["id"]
        available_inventories = pd.DataFrame(
            inventory_api.fetch_inventories(selected_project_id)
        )
        st.session_state["available_inventories"] = available_inventories
        selected = None
        if not available_inventories.empty:
            st.write("Inventare disponibile")
            selected = dataframe_with_selections(
                available_inventories,
                {
                    "name": "Nume",
                    "description": "Descriere",
                    "inventory_method": "Metodă",
                },
                {"owner_id": None, "id": None},
            )

            if not selected.empty:
                st.session_state["selected_inventory"] = selected
                inventory = pd.DataFrame(
                    inventory_api.fetch_all_inventory_items(
                        st.session_state["selected_project"]["id"],
                        selected["id"].values[0],
                    ),
                )
                st.session_state["selected_inventory_items"] = inventory
                st.write(inventory)
            else:
                st.write("Selectează un inventar")
        else:
            st.write("Creează un inventar")
else:
    st.error("Selectează un proiect")
