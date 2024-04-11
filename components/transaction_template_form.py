import uuid
import streamlit as st

from api_client.transaction import create_transaction_template
from components.followup_transaction_template_form import (
    FollowupTransactionTemplateForm,
)


class TransactionTemplateForm:
    def __init__(self):
        self.unique_id = uuid.uuid4().hex
        self.ready = False
        self.name = None
        self.description = None

        self.debtor_account = None
        self.creditor_account = None
        self.currency = None
        self.details = None
        self.main_tx_type = None

        self.main_transaction = None
        self.followup_transactions = []

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "main_transaction": self.main_transaction,
            "followup_transactions": [
                followup_transaction.to_dict()
                for followup_transaction in self.followup_transactions
            ],
        }

    def render(self):
        with st.container(border=True):
            st.title("Creează un tratament contabil")
            self.name = st.text_input("Nume", key=self.unique_id + "nume")

            self.description = st.text_area(
                "Descriere", key=self.unique_id + "description"
            )

            st.header("Tranzacție principală")
            col1, col2 = st.columns(2)
            with col1:
                self.debtor_account = st.text_input(
                    "Cont debitor", key=self.unique_id + "debtor_account"
                )
            with col2:
                self.creditor_account = st.text_input(
                    "Cont creditor", key=self.unique_id + "creditor_account"
                )
            self.currency = st.selectbox("Moneda", ["RON", "EUR"], index=0)
            self.main_tx_type = st.selectbox(
                "Tipul tranzacției",
                [
                    "intrări",
                    "ieșiri",
                    "diverse",
                    "ajustări",
                    "salarii",
                    "TVA-plată",
                    "TVA-încasare",
                    "bancă",
                    "casă",
                    "închidere",
                    "decont",
                ],
                index=0,
                key=self.unique_id + "tx_type",
            )
            self.details = st.text_area("Detalii", key=self.unique_id + "details")

            if all(
                [
                    self.name,
                    self.description,
                    self.debtor_account,
                    self.creditor_account,
                    self.currency,
                    self.details,
                    self.main_tx_type,
                ]
            ):
                self.main_transaction = {
                    "debit_account": self.debtor_account,
                    "credit_account": self.creditor_account,
                    "currency": self.currency,
                    "details": self.details,
                    "tx_type": self.main_tx_type,
                }
            else:
                st.warning("Completează toate câmpurile")

            with st.container():
                for followup_transaction in self.followup_transactions:
                    followup_transaction.render()

                st.button(
                    "Adaugă tranzacție secundara",
                    on_click=lambda: self.followup_transactions.append(
                        FollowupTransactionTemplateForm()
                    ),
                )

            if all(
                [
                    followup_transaction.ready
                    for followup_transaction in self.followup_transactions
                ]
            ):
                self.ready = True

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("Salvează", on_click=lambda: print(self.to_dict())):
                    if self.ready:
                        st.info("Tranzacție salvata")
                        print(self.to_dict())
                        create_transaction_template(1, self.to_dict())
                    else:
                        st.warning("Completează toate câmpurile")
            with col4:
                if st.button("Resetează", on_click=lambda: self.__init__()):
                    print("Anulat")
