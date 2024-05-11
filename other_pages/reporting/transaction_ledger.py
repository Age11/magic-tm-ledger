import streamlit as st
import pandas as pd

from api_client.ledger import fetch_all_transactions

if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None

with st.container(border=True):
    st.title("Registru Jurnal")

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
                "document_type": "Tip document",
                "document_serial_number": "Serie document",
            }
        ).drop(columns=["id", "owner_id", "document_id", "credit_amount"])

        st.write(displayed_transactions)

        st.header("Totaluri:")
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"Total debit: {round(transactions.debit_amount.sum(),2)}")
        with c2:
            st.write(f"Total credit: {round(transactions.credit_amount.sum(),2)}")
