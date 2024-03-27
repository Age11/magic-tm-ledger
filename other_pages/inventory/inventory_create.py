import streamlit as st

from api_client.inventory import create_inventory

st.title("Creează Inventar")


if "selected_project" in st.session_state.keys():
    if not st.session_state["selected_project"] is None:
        with st.form("create-inventory-form"):
            inventory_data = {}
            inventory_data["name"] = st.text_input("Nume")
            inventory_data["description"] = st.text_area("Descriere")
            inventory_data["inventory_method"] = st.selectbox(
                "Metoda Inventar", ["fifo", "lifo", "cmp"], index=0
            )

            if st.form_submit_button("Salvează"):
                if all(inventory_data.values()):
                    create_inventory(
                        st.session_state["selected_project"]["id"], inventory_data
                    )
                    st.info("Inventar creat")
                else:
                    st.error("Toate câmpurile sunt obligatorii")
