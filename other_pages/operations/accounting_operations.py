import streamlit as st

from components.transaction_form import TransactionForm
from components.transaction_from_template_form import TransactionFromTemplateForm

st.title("Articole contabile")

if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None

if not "transaction" in st.session_state.keys():
    st.session_state["transaction"] = None

if not "transaction_from_template" in st.session_state.keys():
    st.session_state["transaction_from_template"] = None

if st.session_state["selected_project"] is not None:
    use_template = st.checkbox("Selectează tratament contabil predefinit")
    if use_template:
        if st.session_state["transaction_from_template"] is None:
            st.session_state["transaction_from_template"] = (
                TransactionFromTemplateForm()
            )
        st.session_state["transaction_from_template"].render()

    else:
        if st.session_state["transaction"] is None:
            st.session_state["transaction"] = TransactionForm()
        st.session_state["transaction"].render()
