from api_client.third_parties import create_organization
from misc.form_labels import organization_input_labels, address_labels, bank_details
import streamlit as st

with st.form("create-client-organization-form", border=True):
    st.header("Creează un nou client")
    organization_data = {}

    organization_data["org_type"] = "client"
    for key in organization_input_labels.keys():
        organization_data[key] = st.text_input(organization_input_labels[key])
    vat = st.selectbox(
        "Mod TVA",
        ["TVA la facturare", "TVA la încasare"],
        index=0,
        key="create_org_vat_mode_selector",
    )
    if vat == "TVA la facturare":
        organization_data["vat_mode"] = "on_invoice"
    if vat == "TVA la încasare":
        organization_data["vat_mode"] = "on_payment"
    st.header("Detalii adresă")
    for key in address_labels.keys():
        organization_data[key] = st.text_input(address_labels[key])
    st.header("Detalii bancare")
    for key in bank_details.keys():
        organization_data[key] = st.text_input(bank_details[key])

    if st.form_submit_button("Salvează"):
        if all(organization_data.values()):
            create_organization(
                st.session_state.selected_project["id"], organization_data
            )
            st.info("Client creat")
        else:
            st.error("Toate câmpurile sunt obligatorii")
