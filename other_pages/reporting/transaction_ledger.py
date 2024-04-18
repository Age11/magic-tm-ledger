import streamlit as st
import pandas as pd

from api_client.ledger import fetch_all_transactions

if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None

st.title("Jurnal Tranzacții")

transactions = pd.DataFrame(
    st.session_state.api_client.reports.fetch_all_transactions()
)

st.write(transactions)
