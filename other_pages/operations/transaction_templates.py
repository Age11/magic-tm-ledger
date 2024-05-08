import streamlit as st

from account_plan import account_plan
from api_client.transaction import fetch_transaction_templates

st.title("Tratamente contabile")

if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None

if st.session_state["selected_project"] is not None:
    available_templates = fetch_transaction_templates(
        st.session_state.selected_project["id"]
    )
    for template in available_templates:
        with st.container(border=True):
            st.header(template['name'])
            st.write(f"Descriere: {template['description']}")
            with st.container(border=True):
                st.write("Tranzacție principală:")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.write(template['main_transaction']['debit_account'])
                    debit_name = account_plan.get(template['main_transaction']['debit_account'])
                    if debit_name is not None:
                        with st.expander("denumire cont", expanded=False):
                            st.write(debit_name)
                with c2:
                    st.write("🟰")
                with c3:
                    st.write(template['main_transaction']['credit_account'])
                    credit_name = account_plan.get(template['main_transaction']['credit_account'])
                    if credit_name is not None:
                        with st.expander("denumire cont", expanded=False):
                            st.write(credit_name)

                st.write(f"Detalii: {template['main_transaction']['details']}")
                st.write(f"Tip tranzacție: {template['main_transaction']['tx_type']}")
                if len(template["followup_transactions"]) > 0:
                    for ft in template["followup_transactions"]:
                        with st.container(border=True):
                            st.write("Tranzacție secundară:")
                            c1, c2 = st.columns(2)
                            with c1:
                                st.write(ft['debit_account'])
                                debit_name = account_plan.get(ft['debit_account'])
                                if debit_name is not None:
                                    with st.expander("denumire cont", expanded=False):
                                        st.write(debit_name)
                            with c2:
                                st.write(ft['credit_account'])
                                credit_name = account_plan.get(ft['credit_account'])
                                if credit_name is not None:
                                    with st.expander("denumire cont", expanded=False):
                                        st.write(credit_name)
                            st.write(f"Detalii: {ft['details']}")
                            st.write(f"Operație: {ft['operation']}")
                            st.write(
                                f"Tip tranzacție: {ft["tx_type"]}"
                            )
