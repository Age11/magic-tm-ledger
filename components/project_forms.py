import pandas as pd
import streamlit as st

from api_client.projects import create_project

from misc.form_labels import (
    organization_input_labels,
    address_labels,
    project_details_labels,
    bank_details,
)


def project_edit(project):
    with st.container():
        data = pd.DataFrame(
            {
                "Câmp": [
                    project_details_labels[k] for k in project_details_labels.keys()
                ],
                "Valoare": [project[k] for k in project_details_labels.keys()],
            }
        )
        edited = st.data_editor(data)
        col1, col2 = st.columns(2)
        with col1:
            st.button(
                "Back",
                on_click=lambda: setattr(
                    st.session_state, "edit_project_details", False
                ),
                key="back_to_project_list_from_edit",
            )
        with col2:
            if st.button("Save", key="save_project_changes_button"):
                print(edited)
                # save changes
                st.success("Changes saved")
