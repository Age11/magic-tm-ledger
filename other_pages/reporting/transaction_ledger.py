import streamlit as st
import pandas as pd

from api_client.ledger import fetch_all_transactions

if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None

with st.container(border=True):
    st.title("Jurnal Tranzacții")

    if "selected_project" not in st.session_state:
        st.session_state["selected_project"] = None

    if st.session_state.selected_project is not None:

        st.session_state["transaction_dates"] = (
            st.session_state.api_client.reports.fetch_available_transaction_dates()
        )

        st.session_state["selected_date"] = st.selectbox(
            "Selectează luna", st.session_state.transaction_dates, index=0
        )

        transactions = pd.DataFrame(
            st.session_state.api_client.reports.fetch_all_transactions_for_date(
                st.session_state.selected_date
            )
        )

        displayed_transactions = transactions.rename(
            columns={
                "transaction_date": "Data",
                "debit_account": "Cont debit",
                "credit_account": "Cont credit",
                "debit_amount": "Sumă",
                "currency": "Monedă",
                "description": "Descriere",
                "details": "Detalii",
                "tx_type": "Tip tranzacție",
            }
        ).drop(columns=["id", "owner_id", "invoice_id", "credit_amount"])

        st.write(displayed_transactions)
