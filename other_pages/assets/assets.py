import pandas as pd
import streamlit as st

from components.dataframe_with_selection import dataframe_with_selections

st.title("Imobilizări")

if "selected_project" in st.session_state.keys():
    if not st.session_state["selected_project"] is None:
        selected_project_id = st.session_state["selected_project"]["id"]
        st.session_state["available_assets"] = pd.DataFrame(
            st.session_state.api_client.assets.fetch_all_assets()
        )

        if not st.session_state.available_assets.empty:
            st.write("Imobilizări disponibile")
            st.write(st.session_state.available_assets)
        else:
            st.write("Creează o imobilizare")
