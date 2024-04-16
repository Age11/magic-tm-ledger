import streamlit as st

import pandas as pd

from components.invoice_form import InflowInvoiceForm


if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None

if not "invoice" in st.session_state.keys():
    st.session_state["invoice"] = None

if not "invoice_client_id" in st.session_state.keys():
    st.session_state["invoice_client_id"] = None

if not "invoice_suppliers" in st.session_state.keys():
    st.session_state["invoice_suppliers"] = None

if not "invoice_items" in st.session_state.keys():
    st.session_state["invoice_items"] = []

if not "invoice_saved" in st.session_state.keys():
    st.session_state["invoice_saved"] = False

if not "available_inventories" in st.session_state.keys():
    st.session_state["available_inventories"] = None

if not "available_templates" in st.session_state.keys():
    st.session_state["available_templates"] = None


st.title("Facturi intrări")

if st.session_state.selected_project is not None:

    st.session_state["invoice_client_id"] = (
        st.session_state.api_client.projects.get_own_organization()[0]["id"]
    )

    st.session_state["invoice_suppliers"] = pd.DataFrame(
        st.session_state.api_client.third_parties.fetch_suppliers()
    )

    st.session_state["available_inventories"] = pd.DataFrame(
        st.session_state.api_client.inventories.fetch()
    )

    st.session_state["available_templates"] = pd.DataFrame(
        st.session_state.api_client.transactions.fetch_transaction_templates_by_type(
            "intrări"
        )
    )

    with st.container():
        st.write("Detalii factură")
        if st.session_state["invoice"] is None:
            st.session_state["invoice"] = InflowInvoiceForm(
                st.session_state["invoice_suppliers"],
                st.session_state["invoice_client_id"],
                st.session_state["available_inventories"],
                st.session_state["available_templates"],
            )
        st.session_state["invoice"].render()

    with st.container():
        if st.button("Factura Noua"):
            st.session_state["invoice"] = None
            st.session_state["invoice_items"] = []
            st.session_state["invoice_saved"] = False
else:
    st.write("Selectează un proiect pentru a vedea facturile")
