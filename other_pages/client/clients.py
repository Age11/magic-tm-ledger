import streamlit as st
from components.dataframe_with_selection import dataframe_with_selections
from misc.form_labels import third_party_list_labels, third_party_list_hidden_columns
import pandas as pd
from api_client.third_parties import fetch_org_clients

st.title("Clienți")
selected_project_id = st.session_state.selected_project["id"]

st.session_state["clients"] = pd.DataFrame(fetch_org_clients(selected_project_id))

if not st.session_state["clients"].empty:
    client = dataframe_with_selections(
        st.session_state["clients"],
        third_party_list_labels,
        hidden_columns=third_party_list_hidden_columns,
    )
    if not client.empty:
        print(f"Selected client: {client["id"][0]}")
        st.session_state["selected_client"] = client
