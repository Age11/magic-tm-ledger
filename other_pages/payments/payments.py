import pandas as pd
import streamlit as st

from components.dataframe_with_selection import dataframe_with_selections

if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None

if st.session_state.selected_project is not None:
    st.title("De Încasat")

    rec = pd.DataFrame(st.session_state.api_client.invoices.fetch_due_receivable())
    # dataframe_with_selections(
    #     rec, column_mapping={"id": "ID", "amount": "Sumă", "due_date": "Data Scadenței"}
    # )

    st.write(rec)

    st.title("De Plătit")
    pay = pd.DataFrame(st.session_state.api_client.invoices.fetch_due_payable())

    st.write(pay)
