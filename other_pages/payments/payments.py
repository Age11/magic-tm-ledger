import pandas as pd
import streamlit as st


if not "selected_project" in st.session_state.keys():
    st.session_state["selected_project"] = None

st.title("Jurnal Plăți")

st.session_state["payment_dates"] = (
    st.session_state.api_client.payments.fetch_available_payment_dates()
)

st.session_state["selected_date"] = st.selectbox(
    "Selectează luna", st.session_state.payment_dates, index=0
)

st.session_state["all_payments"] = (
    st.session_state.api_client.payments.fetch_payments_journal_by_date(
        st.session_state.selected_date
    )
)

if st.session_state.selected_project is not None:
    if "all_payments" in st.session_state.keys():
        pmts = pd.DataFrame(st.session_state.all_payments)
        rec_cash = pmts[
            (pmts["payment_type"] == "încasare") & (pmts["installment_type"] == "casă")
        ]
        rec_bank = pmts[
            (pmts["payment_type"] == "încasare") & (pmts["installment_type"] == "bancă")
        ]
        pay_cash = pmts[
            (pmts["payment_type"] == "plată") & (pmts["installment_type"] == "casă")
        ]
        pay_bank = pmts[
            (pmts["payment_type"] == "plată") & (pmts["installment_type"] == "bancă")
        ]
        st.header("Jurnal de bancă")

        c1, c2 = st.columns(2)
        with c1:
            st.write("Plăți ")
            if pay_bank.empty:
                st.write("Nu sunt înregistrări")
            else:
                st.write(
                    pay_bank.rename(
                        columns={
                            "payment_date": "Dată",
                            "details": "Detalii",
                            "amount": "Sumă",
                            "currency": "Monedă",
                        }
                    ).drop(
                        columns=[
                            "installment_type",
                            "payment_type",
                        ]
                    )
                )

        with c2:
            st.write("Încasări ")
            if rec_bank.empty:
                st.write("Nu sunt înregistrări")
            else:
                st.write(
                    rec_bank.rename(
                        columns={
                            "payment_date": "Dată",
                            "details": "Detalii",
                            "amount": "Sumă",
                            "currency": "Monedă",
                        }
                    ).drop(
                        columns=[
                            "installment_type",
                            "payment_type",
                        ]
                    )
                )
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"Total plăți: {pay_bank['amount'].sum()}")
        with c2:
            st.write(f"Total încasări: {rec_bank['amount'].sum()}")

        st.header("Jurnal de casă")
        c1, c2 = st.columns(2)
        with c1:
            st.write("Plăți ")
            if pay_cash.empty:
                st.write("Nu sunt înregistrări")
            else:
                st.write(
                    pay_cash.rename(
                        columns={
                            "payment_date": "Dată",
                            "details": "Detalii",
                            "amount": "Sumă",
                            "currency": "Monedă",
                        }
                    ).drop(
                        columns=[
                            "installment_type",
                            "payment_type",
                        ]
                    )
                )
        with c2:
            st.write("Încasări ")
            if pay_cash.empty:
                st.write("Nu sunt înregistrări")
            else:
                st.write(
                    rec_cash.rename(
                        columns={
                            "payment_date": "Dată",
                            "details": "Detalii",
                            "amount": "Sumă",
                            "currency": "Monedă",
                        }
                    ).drop(
                        columns=[
                            "installment_type",
                            "payment_type",
                        ]
                    )
                )
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"Total plăți: {pay_cash['amount'].sum()}")

        with c2:
            st.write(f"Total încasări: {rec_cash['amount'].sum()}")
