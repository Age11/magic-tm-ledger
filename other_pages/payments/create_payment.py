import streamlit as st

from components.create_payment_form import CreatePaymentForm

if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None


if st.session_state.selected_project is not None:
    st.title("Crează o plată")
    if "main_create_payment_form" not in st.session_state.keys():
        st.session_state["main_create_payment_form"] = CreatePaymentForm()
    st.session_state["main_create_payment_form"].render()
