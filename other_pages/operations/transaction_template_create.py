import streamlit as st
from components.transaction_template_form import TransactionTemplateForm

if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None

if not "transaction_template_form" in st.session_state.keys():
    st.session_state["transaction_template_form"] = None

if st.session_state["selected_project"] is not None:
    if st.session_state["transaction_template_form"] is None:
        st.session_state["transaction_template_form"] = TransactionTemplateForm()
    st.session_state["transaction_template_form"].render()
