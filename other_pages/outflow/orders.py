import streamlit as st
import pandas as pd
from components.dataframe_with_selection import dataframe_with_selections
import api_client.inventory as inventory_api
from components.order_item_form import OrderItemForm
from components.order_form import OrderForm

if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None

if not "selected_inventory" in st.session_state.keys():
    st.session_state["selected_inventory"] = None

if not "selected_inventory_items" in st.session_state.keys():
    st.session_state["selected_inventory_items"] = None

if not "order_items" in st.session_state.keys():
    st.session_state["order_items"] = []


st.title("Comandă")


if "selected_project" in st.session_state.keys():
    if st.session_state["selected_project"] is not None:

        selected_project_id = st.session_state["selected_project"]["id"]

        st.session_state["invoice_supplier_id"] = (
            st.session_state.api_client.projects.get_own_organization()[0]["id"]
        )

        st.session_state["invoice_clients"] = pd.DataFrame(
            st.session_state.api_client.third_parties.fetch_clients()
        )

        st.session_state["available_inventories"] = pd.DataFrame(
            st.session_state.api_client.inventories.fetch()
        )

        st.session_state["available_templates"] = pd.DataFrame(
            st.session_state.api_client.transactions.fetch_transaction_templates_by_type(
                ["ieșiri"]
            )
        )

        st.session_state["secondary_templates"] = pd.DataFrame(
            st.session_state.api_client.transactions.fetch_transaction_templates_by_type(
                ["descărcare"]
            )
        )

        if "order_form" not in st.session_state.keys():
            st.session_state["order_form"] = OrderForm()
        st.session_state["order_form"].render()

        with st.container():
            st.button(
                "Comanda Noua",
                on_click=lambda: st.session_state["order_form"].__init__(),
            )


# pass search function to searchbox
