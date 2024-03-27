import pandas as pd
import streamlit as st

from api_client.invoices import fetch_invoices

st.title("Facturi")

if not st.session_state.selected_project is None:
    invoices = pd.DataFrame(fetch_invoices(st.session_state.selected_project["id"]))
    if not invoices.empty:
        st.write(invoices)
    else:
        st.write("Nu există facturi")
