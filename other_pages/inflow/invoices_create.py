import streamlit as st
import uuid
import pandas as pd

from api_client import projects, third_parties
from api_client.invoices import create_invoice, update_invoice
from components.invoice_form import InflowInvoiceForm
from components.item_form import ItemForm

if not "invoice" in st.session_state.keys():
    st.session_state["invoice"] = None

if not "invoice_items" in st.session_state.keys():
    st.session_state["invoice_items"] = []

if not "invoice_saved" in st.session_state.keys():
    st.session_state["invoice_saved"] = False


st.title("Facturi intrări")

if not st.session_state.selected_project is None:

    st.session_state["invoice_client_id"] = projects.get_own_organization(
        st.session_state.selected_project["id"]
    )[0]["id"]

    st.session_state["invoice_suppliers"] = pd.DataFrame(
        third_parties.fetch_org_suppliers(st.session_state.selected_project["id"])
    )

    with st.container():
        st.write("Detalii factură")
        if st.session_state["invoice"] is None:
            st.session_state["invoice"] = InflowInvoiceForm(
                uuid.uuid4().hex,
                st.session_state.selected_project["id"],
                st.session_state["invoice_suppliers"],
                st.session_state["invoice_client_id"],
            )
        st.session_state["invoice"].render()

    with st.container():
        if st.session_state["invoice"].saved:
            st.title("Articole factură")
            if st.button("Adauga articol"):
                st.session_state["invoice_items"].append(
                    ItemForm(
                        uuid.uuid4().hex,
                        project_id=st.session_state.selected_project["id"],
                        invoice_id=st.session_state["invoice"].invoice_id,
                        invoice_date=st.session_state["invoice"].invoice_date.strftime(
                            "%Y-%m-%d"
                        ),
                    )
                )

            for item_form in st.session_state["invoice_items"]:
                item_form.render()
        else:
            st.info("Salvează factura pentru a adăuga articole")

    with st.container():
        if st.button("Factura Noua"):
            st.session_state["invoice"] = None
            st.session_state["invoice_items"] = []
            st.session_state["invoice_saved"] = False
