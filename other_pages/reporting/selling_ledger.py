import pandas as pd
import streamlit as st

st.title("Jurnal Vânzări")

if "selected_project" not in st.session_state:
    st.session_state["selected_project"] = None


if st.session_state.selected_project is not None:

    st.session_state["available_dates"] = (
        st.session_state.api_client.reports.fetch_available_balance_dates()
    )

    st.session_state["available_date"] = st.selectbox(
        "Selectează o balanță de verificare", st.session_state.available_dates, index=0
    )

    report = pd.DataFrame(
        st.session_state.api_client.reports.fetch_sales_journal(
            st.session_state["available_date"]
        )
    )
    st.write(
        report
    )

    st.write(f"Total: {report["total"].sum()}")
    st.write(f"Total TVA: {report["vat_amount"].sum()}")
