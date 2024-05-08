import pandas as pd
import streamlit as st

st.title("Jurnal Cumpărări")

if "selected_project" not in st.session_state:
    st.session_state["selected_project"] = None


if st.session_state.selected_project is not None:

    st.session_state["available_dates"] = (
        st.session_state.api_client.reports.fetch_available_balance_dates()
    )

    if len(st.session_state["available_dates"]) > 0:
        st.session_state["available_date"] = st.selectbox(
            "Selectează un jurnal de cumpărări",
            st.session_state.available_dates,
            index=0,
        )

        report = pd.DataFrame(
            st.session_state.api_client.reports.fetch_purchase_journal(
                st.session_state["available_date"]
            )
        ).rename(
            columns={
                "date": "Data",
                "supplier_name": "Furnizor",
                "total": "Total",
                "vat_amount": "Total TVA",
                "regular_amount": "Suma cotă standard",
                "regular_vat_amount": "TVA cotă standard",
                "reduced_amount": "Suma cotă redusă",
                "reduced_vat_amount": "TVA cotă redusă",
                "zero_amount": "Suma scutită",
                "no_vat_amount": "TVA scutită",
                "payed": "Plătit",
            }
        )

        if report.empty:
            st.write("Nu sunt înregistrări")
        else:
            st.write(report.drop(columns=["supplier_vat_code"]))
            st.write(f"Total: {report['Total'].sum()}")
            st.write(f"Total TVA: {report['Total TVA'].sum()}")
    else:
        st.write("Nu sunt înregistrări")
