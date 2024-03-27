import streamlit as st

from api_client.projects import create_project
from misc.form_labels import organization_input_labels, address_labels, bank_details

with st.form("project-create-form"):
    st.title("Creează un nou proiect")
    project_data = {}
    project_data["project_name"] = st.text_input("Nume Proiect")
    project_data["caen_code"] = st.text_input("Cod CAEN")
    st.header("Detalii organizație")
    for key in organization_input_labels.keys():
        project_data[key] = st.text_input(organization_input_labels[key])
    vat = st.selectbox("Mod TVA", ["TVA la facturare", "TVA la încasare"], index=0)
    if vat == "TVA la facturare":
        project_data["vat_mode"] = "on_invoice"
    if vat == "TVA la încasare":
        project_data["vat_mode"] = "on_payment"
    st.header("Detalii adresă")
    for key in address_labels.keys():
        project_data[key] = st.text_input(address_labels[key])
    st.header("Detalii bancare")
    for key in bank_details.keys():
        project_data[key] = st.text_input(bank_details[key])

    if st.form_submit_button("Salvează"):
        if all(project_data.values()):
            create_project(project_data)
            st.info("Proiect creat")
        else:
            st.error("Toate câmpurile sunt obligatorii")
