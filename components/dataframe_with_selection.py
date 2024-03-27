import streamlit as st


def dataframe_with_selections(
    data, column_mapping=None, hidden_columns=None, unique_id=""
):
    df_with_selections = data.copy()
    df_with_selections.insert(0, "Select", False)
    df_with_selections = (
        df_with_selections.rename(columns=column_mapping)
        if column_mapping
        else df_with_selections
    )

    print(data)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={
            **{
                "Selectează": st.column_config.CheckboxColumn(required=True),
            },
            **column_mapping,
            **hidden_columns,
        },
        disabled=data.columns,
        key=unique_id + "data_editor",
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop("Select", axis=1)
