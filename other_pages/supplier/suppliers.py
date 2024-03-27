import streamlit as st
from components.dataframe_with_selection import dataframe_with_selections
from misc.form_labels import third_party_list_hidden_columns, third_party_list_labels
import pandas as pd

from api_client.third_parties import fetch_org_suppliers

st.title("Furnizori")
selected_project_id = st.session_state.selected_project["id"]
st.session_state["suppliers"] = pd.DataFrame(fetch_org_suppliers(selected_project_id))

if not st.session_state["suppliers"].empty:
    supplier = dataframe_with_selections(
        st.session_state["suppliers"],
        third_party_list_labels,
        hidden_columns=third_party_list_hidden_columns,
    )
    st.session_state["selected_supplier"] = supplier
