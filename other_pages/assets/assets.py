import pandas as pd
import streamlit as st

from components.dataframe_with_selection import dataframe_with_selections

st.title("Imobilizări")

if "selected_project" in st.session_state.keys():
    if not st.session_state["selected_project"] is None:
        selected_project_id = st.session_state["selected_project"]["id"]
        st.session_state["available_assets"] = pd.DataFrame(
            st.session_state.api_client.assets.fetch_all_assets()
        )

        if not st.session_state.available_assets.empty:
            st.write("Imobilizări disponibile")
            selected = dataframe_with_selections(
                st.session_state.available_assets,
                column_mapping={
                    "asset_name": "Nume",
                    "description": "Descriere",
                    "initial_value": "Valoare inițială",
                    "inventory_value": "Valoare de inventar",
                    "current_value": "Valoare curentă",
                    "depreciation_method": "Metoda de amortizare",
                    "total_duration": "Durată de amortizare",
                    "rounded_monthly_depreciation": "Amortizare lunară",
                    "remaining_amount": "Valoare rămasă",
                    "deprecated_amount": "Valoare amortizată",
                    "deprecation_start_date": "Data intrare",
                },
                hidden_columns={
                    "id": None,
                    "owner_id": None,
                    "recording_date": None,
                    "acquisition_date": None,
                },
            )

            if not selected.empty:
                st.write(selected)
        else:
            st.write("Creează o imobilizare")
