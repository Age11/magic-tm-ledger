import pandas as pd
import streamlit as st

from api_client.invoices import fetch_invoices

st.title("Facturi")

if not st.session_state.selected_project is None:
    invoices = pd.DataFrame(st.session_state.api_client.invoices.fetch())
    display_invoices = invoices.copy()

    if not invoices.empty:
        st.write(
            display_invoices.rename(
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
    else:
        st.write("Nu există facturi")
else:
    st.write("Selectează un proiect pentru a vedea facturile")
