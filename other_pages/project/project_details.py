import streamlit as st
import pandas as pd

from misc.form_labels import project_details_labels

if "selected_project" not in st.session_state:
    st.error("Selectează un proiect din lista din stânga")

if st.session_state["selected_project"] is not None:
    with st.container():
        st.title(f"Detalii Proiect")
        project = st.session_state["selected_project"]
        for k in project_details_labels.keys():
            print(project_details_labels[k])
            print(project[k])

        data = pd.DataFrame(
            {
                "Câmp": [
                    project_details_labels[k] for k in project_details_labels.keys()
                ],
                "Valoare": [project[k] for k in project_details_labels.keys()],
            }
        )

        st.dataframe(data)
