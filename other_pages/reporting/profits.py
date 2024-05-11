import streamlit as st

with st.container(border=True):
    st.title("Profit sau pierdere")

    if "selected_project" not in st.session_state:
        st.session_state["selected_project"] = None

    if st.session_state.selected_project is not None:

        st.session_state["transaction_dates"] = (
            st.session_state.api_client.reports.fetch_available_transaction_dates()
        )

        st.session_state["selected_date"] = st.selectbox(
            "Selectează luna", st.session_state.transaction_dates, index=0
        )

    result = st.session_state.api_client.account_balance.fetch_current_profit_or_loss(
        st.session_state.selected_date
    )
    with st.container(border=True):
        st.header(result)
