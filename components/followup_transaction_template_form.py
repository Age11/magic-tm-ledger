import uuid

import streamlit as st


class FollowupTransactionTemplateForm:

    def __init__(self):
        self.unique_id = uuid.uuid4().hex
        self.debit_account = None
        self.credit_account = None
        self.operation = None
        self.details = None
        self.ready = False

    def to_dict(self):
        return {
            "debit_account": self.debit_account,
            "credit_account": self.credit_account,
            "operation": self.operation,
            "details": self.details,
        }

    def render(self):
        with st.container(border=True):
            st.header("Tranzacție secundară")
            col1, col2 = st.columns(2)

            with col1:
                self.debit_account = st.text_input(
                    "Cont debitor", key=self.unique_id + "debtor_account"
                )
            with col2:
                self.credit_account = st.text_input(
                    "Cont creditor", key=self.unique_id + "creditor_account"
                )

            self.operation = st.text_input("Operație", key=self.unique_id + "operation")

            self.details = st.text_area("Detalii", key=self.unique_id + "description")

            if all(
                [
                    self.debit_account,
                    self.credit_account,
                    self.operation,
                    self.details,
                ]
            ):
                self.ready = True
            else:
                self.ready = False
                st.warning("Completează toate câmpurile")
