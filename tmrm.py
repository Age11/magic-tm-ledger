import pandas as pd
import streamlit as st
import api_client.projects as projects_api

from st_pages import Page, show_pages, add_page_title, Section
from api.client import Client


if "selected_project" not in st.session_state:
    st.session_state["selected_project"] = None

if "api_client" not in st.session_state:
    st.session_state["api_client"] = None

st.session_state["projects"] = pd.DataFrame(projects_api.fetch_projects())

add_page_title("Proiecte")

show_pages(
    [
        Page("tmrm.py", "Proiecte", "🏠"),
        Section(name="Gestionați Proiecte", icon="💼"),
        Page("other_pages/project/project_details.py", "Detalii Proiect"),
        Page("other_pages/project/project_create.py", "Creează Proiect"),
        Section(name="Intrări", icon="🛒"),
        Page("other_pages/inflow/invoices.py", "Listă Facturi"),
        Page("other_pages/inflow/invoices_create.py", "Încarcă Factură"),
        Section(name="Ieșiri", icon="💰"),
        Page("other_pages/outflow/orders.py", "Vânzări"),
        Section(name="Casă / Bancă", icon="💳"),
        Page("other_pages/payments/payments.py", "Plați"),
        Section(name="Operațiuni stocuri", icon="📦"),
        Page("other_pages/inventory/inventory.py", "Gestiuni"),
        Page("other_pages/inventory/inventory_create.py", "Creează Gestiune"),
        Page(
            "other_pages/inventory/inventory_create_item.py",
            "Adaugă Produs in Gestiune",
        ),
        Section(name="Articole contabile", icon="🖊️"),
        Page("other_pages/operations/accounting_operations.py", "Articole contabile"),
        Section(name="Rapoarte", icon="📚"),
        Page("other_pages/reporting/transaction_ledger.py", "Registru Tranzacții"),
        Page("other_pages/reporting/account_balance.py", "Balanță de verificare"),
        Page("other_pages/reporting/buying_ledger.py", "Jurnal Cumpărări"),
        Page("other_pages/reporting/selling_ledger.py", "Jurnal Vânzări"),
        Page("other_pages/reporting/profits.py", "Situație Profit sau Pierdere"),
        Section(name="Tratamente contabile", icon="🧮"),
        Page("other_pages/operations/transaction_templates.py", "Șabloane Tranzacții"),
        Page(
            "other_pages/operations/transaction_template_create.py",
            "Creează Șabloane Tranzacții",
        ),
        Section(name="Gestionați Furnizori", icon="🚚"),
        Page("other_pages/supplier/suppliers.py", "Listă Furnizori"),
        Page("other_pages/supplier/supplier_details.py", "Detalii Furnizor"),
        Page("other_pages/supplier/supplier_create.py", "Creează Furnizori"),
        Section(name="Gestionați Clienți", icon="🤝"),
        Page("other_pages/client/clients.py", "Listă Clienți"),
        Page("other_pages/client/client_details.py", "Detalii Client"),
        Page("other_pages/client/client_create.py", "Creează Clienți"),
    ]
)

if not st.session_state["projects"].empty:
    with st.container():
        project_names = [prj for prj in st.session_state.projects.project_name]
        selected_project = st.selectbox(
            "Selectează un proiect",
            options=range(len(project_names)),
            format_func=lambda x: project_names[x],
            index=0,
        )
        st.session_state["selected_project"] = st.session_state.projects.iloc[
            selected_project
        ]
        selected_project_id = st.session_state.selected_project.id

        st.session_state["api_client"] = Client(selected_project_id)
        if st.button("Selectează"):
            st.info(f"Proiect selectat")
            print(f"Selected project: {st.session_state.selected_project.id}")
