import streamlit as st
import pandas as pd

from api_client.ledger import fetch_all_transactions

if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None

st.title("Jurnal Tranzacții")

transactions = pd.DataFrame(
    fetch_all_transactions(st.session_state.selected_project["id"])
)

st.write(transactions)
