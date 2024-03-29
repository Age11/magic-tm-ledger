import pandas as pd
import streamlit as st

from api_client.ledger import fetch_account_balances

if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None

st.title("Fișa conturi")
account_balances = pd.DataFrame(
    fetch_account_balances(st.session_state["selected_project"]["id"])
)

st.write(account_balances)
