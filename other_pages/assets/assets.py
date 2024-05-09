import pandas as pd
import streamlit as st

from components.dataframe_with_selection import dataframe_with_selections
from components.tft_form_custom_templates import (
    TransactionFromTemplateFormCustomTemplates,
)
from components.transaction_from_template_form import TransactionFromTemplateForm

st.title("Imobilizări")
st.session_state["available_templates"] = pd.DataFrame(
    st.session_state.api_client.transactions.fetch_transaction_templates_by_type(
        ["amortizări"]
    )
)
if "selected_project" in st.session_state.keys():
    if not st.session_state["selected_project"] is None:
        selected_project_id = st.session_state["selected_project"]["id"]
        st.session_state["available_assets"] = pd.DataFrame(
            st.session_state.api_client.assets.fetch_all_assets()
        )

        if not st.session_state.available_assets.empty:
            selected = dataframe_with_selections(
                st.session_state.available_assets,
                column_mapping={
                    "asset_name": "Nume",
                    "description": "Descriere",
                    "inventory_value": "Valoare de inventar",
                    "current_value": "Valoare curentă",
                    "depreciation_method": "Metoda de amortizare",
                    "total_duration": "Durată de amortizare",
                    "rounded_monthly_amount": "Amortizare lunară",
                    "remaining_duration": "Durată rămasă",
                    "remaining_amount": "Valoare rămasă",
                    "deprecated_amount": "Valoare amortizată",
                    "deprecation_start_date": "Data intrare",
                },
                hidden_columns={
                    "id": None,
                    "owner_id": None,
                    "recording_date": None,
                    "acquisition_date": None,
                    "initial_value": None,
                },
            )

            if not selected.empty:
                with st.container(border=True):
                    st.write("Înregistrează amortizare")
                    st.session_state["template_form"] = (
                        TransactionFromTemplateFormCustomTemplates()
                    )
                    st.session_state["template_form"].render()
        else:
            st.write("Creează o imobilizare")
