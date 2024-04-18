import pandas as pd
import streamlit as st

from api_client.ledger import fetch_account_balances

if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None

st.title("Balanță de verificare")

if st.session_state.selected_project is not None:

    st.session_state["available_balances"] = (
        st.session_state.api_client.reports.fetch_available_balance_dates()
    )

    st.session_state["current_balance_date"] = st.selectbox(
        "Selectează o balanță de verificare",
        st.session_state.available_balances,
        index=0,
    )
    st.session_state["account_balance"] = pd.DataFrame(
        st.session_state.api_client.reports.fetch_account_balances_by_date(
            st.session_state.current_balance_date
        )
    )

    st.write(st.session_state.account_balance)

    if (~st.session_state.account_balance["processed"]).all():

        st.button(
            "Închide luna",
            on_click=lambda: st.session_state.api_client.reports.close_month(
                st.session_state.current_balance_date
            ),
        )
