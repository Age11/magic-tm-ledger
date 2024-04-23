import streamlit as st

st.title("Raportare Profit sau Pierdere")

if "selected_project" not in st.session_state:
    st.session_state["selected_project"] = None


if st.session_state.selected_project is not None:
    result = st.session_state.api_client.account_balance.fetch_current_profit_or_loss()
    st.write(result)
