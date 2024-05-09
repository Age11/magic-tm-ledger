import uuid
from datetime import datetime
import streamlit as st


class CreatePaymentForm:
    def __init__(self, transaction_id="N/A"):
        self.unique_id = uuid.uuid4().hex
        self.saved = False
        self.payment_date = None
        self.amount = None
        self.payment_date = None
        self.payment_due_date = None
        self.payment_type = None
        self.currency = None
        self.transaction_id = transaction_id

    def save_payment(self):
        if all(
            [
                self.payment_date,
                self.payment_due_date,
                self.amount,
                self.payment_type,
                self.currency,
                self.transaction_id,
            ]
        ):

            st.session_state.api_client.payments.create_payment(
                {
                    "payment_date": self.payment_date.strftime("%Y-%m-%d"),
                    "due_date": self.payment_due_date.strftime("%Y-%m-%d"),
                    "amount_due": self.amount,
                    "payment_status": "restantă",
                    "payment_type": self.payment_type,
                    "currency": self.currency,
                    "transaction_id": self.transaction_id,
                }
            )
            self.saved = True
        else:
            st.error("Completați toate câmpurile")

    def render(self):
        with st.container(border=True):
            self.payment_date = st.date_input(
                "Data plății", key=self.unique_id + "payment_date"
            )
            self.payment_due_date = st.date_input(
                "Data scadenței", key=self.unique_id + "payment_due_date"
            )
            self.payment_type = st.selectbox(
                "Tipul plății",
                ["plată", "încasare"],
                index=0,
                key=self.unique_id + "payment_type",
            )
            self.currency = st.selectbox(
                "Moneda",
                ["RON", "EUR"],
                index=0,
                key=self.unique_id + "payment_currency",
            )
            self.amount = st.number_input("Suma", key=self.unique_id + "payment_amount")

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                if self.saved:
                    st.success("Plata a fost salvată")
                else:
                    st.button(
                        "Salvează",
                        key=self.unique_id + "sv",
                        on_click=self.save_payment,
                    )
