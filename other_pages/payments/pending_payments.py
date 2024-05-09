import uuid

import pandas as pd
import streamlit as st

from components.billing_form import BillingForm

if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None


st.session_state["available_templates"] = pd.DataFrame(
    st.session_state.api_client.transactions.fetch_transaction_templates_by_type(
        ["încasare", "plată"]
    )
)

st.session_state["payment_dates"] = (
    st.session_state.api_client.payments.fetch_available_payment_dates()
)

st.session_state["selected_date"] = st.selectbox(
    "Selectează un jurnal de cumpărări", st.session_state.payment_dates, index=0
)

st.session_state["receivables"] = (
    st.session_state.api_client.payments.fetch_due_receivable_by_date(
        st.session_state.selected_date
    )
)

st.session_state["payable"] = (
    st.session_state.api_client.payments.fetch_due_payable_by_date(
        st.session_state.selected_date
    )
)


if st.session_state.selected_project is not None:
    if "receivable_billing_form" not in st.session_state.keys():
        st.session_state["receivable_billing_form"] = BillingForm()
    st.session_state["receivable_billing_form"].data = st.session_state["receivables"]
    st.title("De Încasat")

    st.session_state["receivable_billing_form"].render()

    st.title("De Plătit")
    if "payable_billing_form" not in st.session_state.keys():
        st.session_state["payable_billing_form"] = BillingForm()
    st.session_state["payable_billing_form"].data = st.session_state["payable"]

    st.session_state["payable_billing_form"].render()
