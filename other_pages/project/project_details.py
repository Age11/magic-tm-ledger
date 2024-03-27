import streamlit as st
import pandas as pd

from misc.form_labels import project_details_labels

with st.container():
    st.title("Detalii Proiect")
    project = st.session_state["selected_project"]
    st.text(f"Nume Proiect: {project['project_name']}")
    for k in project_details_labels.keys():
        print(project_details_labels[k])
        print(project[k])

    data = pd.DataFrame(
        {
            "Câmp": [project_details_labels[k] for k in project_details_labels.keys()],
            "Valoare": [project[k] for k in project_details_labels.keys()],
        }
    )

    st.dataframe(data)
