import pandas as pd
import streamlit as st
import api_client.projects as projects_api


from st_pages import Page, show_pages, add_page_title, Section

add_page_title("Proiecte")

show_pages(
    [
        Page("tmrm.py", "Proiecte", "🏠"),
        Section(name="Gestionați Proiecte", icon="💼"),
        Page("other_pages/project/project_details.py", "Detalii Proiect"),
        Page("other_pages/project/project_create.py", "Creează Proiect"),
        Section(name="Gestionați Furnizori", icon="🚚"),
        Page("other_pages/supplier/suppliers.py", "Listă Furnizori"),
        Page("other_pages/supplier/supplier_details.py", "Detalii Furnizor"),
        Page("other_pages/supplier/supplier_create.py", "Creează Furnizori"),
        Section(name="Gestionați Clienți", icon="🤝"),
        Page("other_pages/client/clients.py", "Listă Clienți"),
        Page("other_pages/client/client_details.py", "Detalii Client"),
        Page("other_pages/client/client_create.py", "Creează Clienți"),
        Section(name="Operațiuni stocuri", icon="📦"),
        Page("other_pages/inventory/inventory.py", "Inventar"),
        Page("other_pages/inventory/inventory_create.py", "Creează Inventar"),
        Page("other_pages/inventory/inventory_create_item.py", "Adaugă Produs in inventar"),
        Section(name="Intrări", icon="🛒"),
        Page("other_pages/inflow/invoices.py", "Listă Facturi"),
        Page("other_pages/inflow/invoices_create.py", "Încarcă Factură"),

    ]
)

st.session_state["projects"] = pd.DataFrame(projects_api.fetch_projects())
print(f"fetched the following projects: {'\n'} {st.session_state["projects"]}")

if not st.session_state["projects"].empty:
    with st.container():
        project_names = [prj for prj in st.session_state["projects"]["project_name"]]
        print(project_names)
        selected_project = st.selectbox(
            "Selectează un proiect",
            options=range(len(project_names)),
            format_func=lambda x: project_names[x],
            index=0,
        )
        st.session_state["selected_project"] = st.session_state["projects"].iloc[
            selected_project
        ]
        selected_project_id = st.session_state["selected_project"]["id"]
        if st.button("Selectează"):
            st.info(f"Proiect selectat")
            print(f"Selected project: {st.session_state['selected_project']['id']}")




