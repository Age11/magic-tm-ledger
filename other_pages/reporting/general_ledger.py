import pandas as pd
import streamlit as st

with st.container(border=True):
    st.title("Cartea mare")

    if "selected_project" not in st.session_state:
        st.session_state["selected_project"] = None

    if st.session_state.selected_project is not None:

        st.session_state["transaction_dates"] = (
            st.session_state.api_client.reports.fetch_available_transaction_dates()
        )

        st.session_state["selected_date"] = st.selectbox(
            "Selectează luna", st.session_state.transaction_dates, index=0
        )

        st.session_state["account"] = st.text_input("Cont")

        if st.button("Fișă cont"):
            if st.session_state["account"] == "":
                st.error("Introduceți un cont!")
            else:
                report = st.session_state.api_client.reports.fetch_general_ledger(
                    st.session_state["selected_date"], st.session_state["account"]
                )
                c1, c2 = st.columns(2)
                with c1:
                    st.header("Debit")
                    dbt = pd.DataFrame(report["debit"])
                    if dbt.empty:
                        st.write("Nu sunt înregistrări")
                    else:
                        st.write(dbt)
                with c2:
                    st.header("Credit")
                    cdt = pd.DataFrame(report["credit"])
                    if cdt.empty:
                        st.write("Nu sunt înregistrări")
                    else:
                        st.write(cdt)
