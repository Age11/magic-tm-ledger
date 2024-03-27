import uuid

import streamlit as st

from api_client.inventory import create_inventory_item


st.title(f"Adaugă un produs în inventar {st.session_state["selected_inventory"].values[0][1]}")

if "selected_project" in st.session_state.keys():
    if not st.session_state["selected_project"] is None:
        with st.form("create-inventory-form"):

            inventory_item_data = {}
            inventory_item_data["name"] = st.text_input("Nume")
            inventory_item_data["description"] = st.text_area("Descriere")
            inventory_item_data["quantity"] = st.number_input("Cantitate", min_value=1)
            inventory_item_data["measurement_unit"] = st.text_input("Unitate de măsură")
            inventory_item_data["acquisition_price"] = st.number_input(
                "Preț de achiziție", min_value=0
            )
            inventory_item_data["vat_rate"] = st.number_input(
                "Rată TVA", min_value=0, max_value=100
            )

            #TODO remove hack
            inventory_item_data["invoice_id"] = -1

            if st.form_submit_button("Salvează"):
                if all(inventory_item_data.values()):
                    create_inventory_item(
                        st.session_state["selected_project"]["id"], st.session_state["selected_inventory"].iloc[0]['id'], inventory_item_data
                    )
                    st.info("Produs adăugat în inventar")


                else:
                    st.error("Toate câmpurile sunt obligatorii")
