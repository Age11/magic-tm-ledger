import pandas as pd
import streamlit as st
from components.dataframe_with_selection import dataframe_with_selections
import api_client.inventory as inventory_api

st.title("Gestiuni")

if "selected_project" in st.session_state.keys():
    if not st.session_state["selected_project"] is None:
        selected_project_id = st.session_state["selected_project"]["id"]
        available_inventories = pd.DataFrame(
            inventory_api.fetch_inventories(selected_project_id)
        )
        st.session_state["available_inventories"] = available_inventories
        selected = None
        if not available_inventories.empty:
            st.write("Gestiuni disponibile")
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
                st.write(
                    inventory.rename(
                        columns={
                            "name": "Nume",
                            "description": "Descriere",
                            "quantity": "Cantitate",
                            "measurement_unit": "Unitate",
                            "acquisition_price": "Preț unitar achiziție",
                            "sale_price": "Preț unitar vânzare",
                            "currency": "Monedă",
                            "vat_rate": "TVA",
                            "total_value": "Valoare totală",
                            "acquisition_date": "Data achiziției",
                        }
                    ).drop(
                        columns=[
                            "id",
                            "inventory_id",
                            "invoice_id",
                            "inventory_id",
                        ]
                    )
                )
            else:
                st.write("Selectează o gestiune")
        else:
            st.write("Creează o gestiune")
else:
    st.error("Selectează un proiect")
