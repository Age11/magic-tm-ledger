import streamlit as st

from api_client.transaction import fetch_transaction_templates

st.title("Tratamente contabile")

if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None

if st.session_state["selected_project"] is not None:
    available_templates = fetch_transaction_templates(
        st.session_state.selected_project["id"]
    )
    st.write(available_templates)
