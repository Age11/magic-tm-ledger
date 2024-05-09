import pandas as pd
import streamlit as st

from api_client.invoices import fetch_invoices

st.title("Facturi")

if not st.session_state.selected_project is None:

    st.session_state["invoice_dates"] = (
        st.session_state.api_client.invoices.fetch_available_dates()
    )

    st.session_state["selected_date"] = st.selectbox(
        "Selectează luna", st.session_state.invoice_dates, index=0
    )

    st.session_state["all_invoices"] = (
        st.session_state.api_client.invoices.fetch_all_by_date(
            st.session_state.selected_date
        )
    )
    invoices = pd.DataFrame(st.session_state.all_invoices)

    in_invs = invoices[invoices["invoice_type"] == "primită"]
    out_invs = invoices[invoices["invoice_type"] == "emisă"]

    st.header("Facturi primite")
    if not in_invs.empty:
        st.write(
            in_invs.rename(
                columns={
                    "serial_number": "Seria",
                    "invoice_date": "Data facturii",
                    "supplier_name": "Furnizor",
                    "sup_nrc": "NRC Furnizor",
                    "client_name": "Client",
                    "cli_nrc": "NRC Client",
                    "amount": "Sumă",
                    "vat_amount": "TVA",
                    "total_amount": "Total",
                    "currency": "Monedă",
                    "invoice_type": "Tip",
                    "issuer_name": "Emitent",
                }
            ).drop(columns=["id", "owner_id", "supplier_id", "client_id"])
        )
        st.write(f"Total facturi primite: {in_invs['total_amount'].sum()}")
    else:
        st.write("Nu există facturi")

    st.header("Facturi primite")
    if not out_invs.empty:
        st.write(
            out_invs.rename(
                columns={
                    "serial_number": "Seria",
                    "invoice_date": "Data facturii",
                    "supplier_name": "Furnizor",
                    "sup_nrc": "NRC Furnizor",
                    "client_name": "Client",
                    "cli_nrc": "NRC Client",
                    "amount": "Sumă",
                    "vat_amount": "TVA",
                    "total_amount": "Total",
                    "currency": "Monedă",
                    "invoice_type": "Tip",
                    "issuer_name": "Emitent",
                }
            ).drop(columns=["id", "owner_id", "supplier_id", "client_id"])
        )
        st.write(f"Total facturi emise: {out_invs['total_amount'].sum()}")
    else:
        st.write("Nu există facturi")
else:
    st.write("Selectează un proiect pentru a vedea facturile")
