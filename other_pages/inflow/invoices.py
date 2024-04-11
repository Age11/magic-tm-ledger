import pandas as pd
import streamlit as st

from api_client.invoices import fetch_invoices

st.title("Facturi")

if not st.session_state.selected_project is None:
    invoices = pd.DataFrame(st.session_state.api_client.invoices.fetch())
    if not invoices.empty:
        st.write(invoices)
    else:
        st.write("Nu există facturi")
else:
    st.write("Selectează un proiect pentru a vedea facturile")
