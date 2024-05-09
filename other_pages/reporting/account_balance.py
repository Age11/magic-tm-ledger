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

    show_df = st.session_state.account_balance.copy()

    st.write(
        show_df.rename(
            columns={
                "analytical_account": "Cont",
                "initial_debit": "Sold Inițial Debitor (an)",
                "initial_credit": "Sold Inițial Creditor (an)",
                "cumulated_debit": "Sold Debitor Cumulat",
                "cumulated_credit": "Sold Creditor cumulat",
                "current_turnover_debit": "Rulaj debitor perioadă",
                "current_turnover_credit": "Rulaj creditor perioadă",
                "total_debit_balance": "Sume Totale Debitoare",
                "total_credit_balance": "Sume Totale Creditoare",
                "final_debit_balance": "Sold Final Debitor",
                "final_credit_balance": "Sold Final Creditor",
                "processed": "Intrare închisă",
            },
        ).drop(
            columns=[
                "id",
                "balance_date",
                "owner_id",
            ]
        ),
    )

    st.header("Totaluri:")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.write(
            f"Sold inițial debitor: {round(st.session_state.account_balance.initial_debit.sum(),2)}"
        )
        st.write(
            f"Sold inițial creditor: {round(st.session_state.account_balance.initial_credit.sum(),2)}"
        )
    with c2:
        st.write(
            f"Sold debitor cumulat: {round(st.session_state.account_balance.cumulated_debit.sum(),2)}"
        )
        st.write(
            f"Sold creditor cumulat: {round(st.session_state.account_balance.cumulated_credit.sum(),2)}"
        )
    with c3:
        st.write(
            f"Rulaj debitor perioadă: {round(st.session_state.account_balance.current_turnover_debit.sum(),2)}"
        )

        st.write(
            f"Rulaj creditor perioadă: {round(st.session_state.account_balance.current_turnover_credit.sum(),2)}"
        )
    with c4:
        st.write(
            f"Sume totale debitoare: {round(st.session_state.account_balance.total_debit_balance.sum(),2)}"
        )
        st.write(
            f"Sume totale creditoare: {round(st.session_state.account_balance.total_credit_balance.sum(),2)}"
        )

    if (~st.session_state.account_balance["processed"]).all():

        st.button(
            "Închide luna",
            on_click=lambda: st.session_state.api_client.reports.close_month(
                st.session_state.current_balance_date
            ),
        )
