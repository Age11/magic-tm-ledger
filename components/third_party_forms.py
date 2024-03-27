import streamlit as st

from api_client.third_parties import (
    fetch_address,
    fetch_banking_details,
    fetch_organization_details,
    create_organization,
)
from misc.form_labels import organization_input_labels, address_labels, bank_details


def dataframe_with_selections(data):
    df_with_selections = data.copy()
    df_with_selections.insert(0, "Select", False)
    print(data)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Selectează": st.column_config.CheckboxColumn(required=True)},
        disabled=data.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop("Select", axis=1)


def display_organizations_screen(orgs):
    if "selected_third_party" not in st.session_state:
        st.session_state.selected_third_party = None

    if "show_organization_details_form" not in st.session_state:
        st.session_state.show_organization_details_form = False

    if "show_create_organization_form" not in st.session_state:
        st.session_state.show_create_organization_form = False

    if not orgs.empty:

        with st.container():

            if st.session_state.show_organization_details_form:
                organization_details_screen()
            elif st.session_state.show_create_organization_form:
                create_organization_form()
            else:
                orgs_to_display = orgs[["organization_name", "cif"]]
                selected_org = dataframe_with_selections(
                    orgs_to_display.rename(
                        columns={
                            "organization_name": "Nume Organizație",
                            "cif": "C.I.F.",
                        }
                    )
                )
                if selected_org.empty:
                    st.info("Selectează un terț din listă")
                else:
                    st.session_state.selected_third_party = orgs[
                        orgs["cif"] == selected_org["C.I.F."]
                    ]
                col1, col2 = st.columns(2)
                with col1:
                    st.button(
                        "Detalii",
                        on_click=lambda: setattr(
                            st.session_state, "show_organization_details_form", True
                        ),
                    )
                with col2:
                    st.button(
                        "Creează",
                        on_click=lambda: setattr(
                            st.session_state, "show_create_organization_form", True
                        ),
                    )
    else:
        st.info("Nu există terți de afișat")


def organization_details_screen():
    pass
    # with st.container():
    #     if st.session_state.selected_third_party is not None:
    #         organization = st.session_state.selected_third_party
    #         print(type(organization["address_id"][0]))
    #     else:
    #         st.info("Selectează un terț din listă")
    #
    #     organization_detail = fetch_organization_details(
    #         st.session_state.selected_project["id"], organization["id"][0]
    #     )
    #     print(organization_detail)
    #
    #     address = fetch_address(
    #         st.session_state.selected_project["id"], organization["address_id"][0]
    #     )
    #     print(address)
    #     banking_details = fetch_banking_details(
    #         st.session_state.selected_project["id"],
    #         organization["banking_details_id"][0],
    #     )
    #     print(banking_details)
    #
    #     st.write(organization_detail)
    #     st.write(address)
    #     st.write(banking_details)
    #
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         st.button(
    #             "Back",
    #             on_click=lambda: setattr(
    #                 st.session_state,
    #                 False,
    #             ),
    #             id="back_to_organization_list_from_details",
    #         )
    #     with col2:
    #         st.button(
    #             "Edit",
    #             on_click=lambda: setattr(
    #                 st.session_state,
    #                 "show_edit_organization_form",
    #                 True,
    #             ),
    #             id="edit_organization_details",
    #         )


def create_organization_form():
    count = 0
