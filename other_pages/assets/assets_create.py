import streamlit as st

st.title("Adaugă Imobilizare")


with st.form(border=True, key="create-asset-form"):
    asset_data = {}
    asset_data["asset_name"] = st.text_input("Nume")
    asset_data["description"] = st.text_area("Descriere")

    asset_data["initial_value"] = st.number_input("Valoare inițială", min_value=0.0)
    asset_data["inventory_value"] = st.number_input(
        "Valoare de inventar", min_value=0.0
    )
    asset_data["current_value"] = st.number_input("Valoare curentă", min_value=0.0)
    asset_data["depreciation_method"] = st.selectbox(
        "Metoda de amortizare",
        [
            "liniară",
            "accelerată",
            "degresivă",
        ],
    )
    asset_data["acquisition_date"] = st.date_input("Data achiziției").strftime("%Y-%m")
    asset_data["total_duration"] = st.number_input("Durata totală", min_value=0.0)
    asset_data["recording_date"] = st.date_input("Data înregistrării").strftime("%Y-%m")

    if st.form_submit_button("Salvează"):
        if all(asset_data.values()):
            st.session_state.api_client.assets.create_asset(asset_data)
            st.info("Imobilizare creată")
        else:
            st.error("Toate câmpurile sunt obligatorii")
