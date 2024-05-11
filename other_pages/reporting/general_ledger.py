import pandas as pd
import streamlit as st

with st.container(border=True):
    st.title("Cartea mare")

    if "selected_project" not in st.session_state:
        st.session_state["selected_project"] = None

    if st.session_state.selected_project is not None:

        st.session_state["transaction_dates"] = (
            st.session_state.api_client.reports.fetch_available_transaction_dates()
        )

        st.session_state["selected_date"] = st.selectbox(
            "Selectează luna", st.session_state.transaction_dates, index=0
        )

        st.session_state["account"] = st.text_input("Cont")

        total_debit = 0
        total_credit = 0

        if st.button("Fișă cont"):
            if st.session_state["account"] == "":
                st.error("Introduceți un cont!")
            else:
                st.header(f"Contul {st.session_state.account}")
                report = st.session_state.api_client.reports.fetch_general_ledger(
                    st.session_state["selected_date"], st.session_state["account"]
                )
                c1, c2 = st.columns(2)
                with c1:
                    st.header("Debit ")
                    dbt = pd.DataFrame(report["debit"])
                    if dbt.empty:
                        st.write("Nu sunt înregistrări")

                    else:
                        total_debit = dbt["debit"].sum()
                        st.write(
                            dbt.rename(columns={"date": "Dată", "debit": "Sumă"}).drop(
                                columns=["account"]
                            )
                        )
                        st.write(f"Total debitor: {total_debit}")

                with c2:
                    st.header("Credit")
                    cdt = pd.DataFrame(report["credit"])
                    if cdt.empty:
                        st.write("Nu sunt înregistrări")

                    else:
                        total_credit = cdt["credit"].sum()
                        st.write(
                            cdt.rename(columns={"date": "Dată", "credit": "Sumă"}).drop(
                                columns=["account"]
                            )
                        )
                        st.write(f"Total creditor: {total_credit}")

                final_balance = total_debit - total_credit
                if final_balance > 0:
                    st.header(f"Sold final debitor: {abs(final_balance)}")
                elif final_balance < 0:
                    st.header(f"Sold final creditor: {abs(final_balance)}")
                else:
                    st.header("Sold final: 0")
