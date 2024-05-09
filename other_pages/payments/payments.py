import pandas as pd
import streamlit as st


if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None

st.title("Jurnal Plăți")

st.session_state["payment_dates"] = (
    st.session_state.api_client.payments.fetch_available_payment_dates()
)

st.session_state["selected_date"] = st.selectbox(
    "Selectează un jurnal de cumpărări", st.session_state.payment_dates, index=0
)

st.session_state["all_payments"] = (
    st.session_state.api_client.payments.fetch_all_payments_by_date(
        st.session_state.selected_date
    )
)

if st.session_state.selected_project is not None:
    if "all_payments" in st.session_state.keys():
        pmts = pd.DataFrame(st.session_state.all_payments)
        rec = pmts[pmts["payment_type"] == "încasare"]
        pay = pmts[pmts["payment_type"] == "plată"]
        st.header("Încasări")
        st.write(
            rec.rename(
                columns={
                    "payment_date": "Dată",
                    "due_date": "Scadență",
                    "status": "Status",
                    "Details": "Detalii",
                    "amount_due": "Sumă",
                    "pending_amount": "Sumă restantă",
                    "currency": "Monedă",
                }
            ).drop(
                columns=[
                    "id",
                    "owner_id",
                    "payment_type",
                    "transaction_id",
                    "invoice_id",
                    "amount_paid",
                ]
            )
        )
        st.write(f"Total încasări: {rec['amount_due'].sum()}")

        st.header("Plăți")
        st.write(
            pay.rename(
                columns={
                    "payment_date": "Dată",
                    "due_date": "Scadență",
                    "status": "Status",
                    "Details": "Detalii",
                    "amount_due": "Sumă",
                    "pending_amount": "Sumă restantă",
                    "currency": "Monedă",
                }
            ).drop(
                columns=[
                    "id",
                    "owner_id",
                    "payment_type",
                    "transaction_id",
                    "invoice_id",
                    "amount_paid",
                ]
            )
        )
        st.write(f"Total plăți: {pay['amount_due'].sum()}")
