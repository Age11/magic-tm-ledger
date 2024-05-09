import uuid

import pandas as pd
import streamlit as st

from api_client.transaction import (
    fetch_transaction_templates,
    create_transaction_from_template,
)
from components.create_payment_form import CreatePaymentForm
from components.transaction_card import TransactionCard


class TransactionFromTemplateFormCustomTemplates:
    def __init__(self):
        self.unique_id = uuid.uuid4().hex
        self.amount = None
        self.available_templates = None
        self.document_serial_number = "N/A"
        self.saved = False
        self.transaction_id = None

    def save(self):
        if all([self.amount, self.selected_template, self.selected_date]):
            txns = create_transaction_from_template(
                project_id=st.session_state["selected_project"]["id"],
                transaction_template_id=self.available_templates.loc[
                    self.available_templates["name"] == self.selected_template,
                    "id",
                ].iloc[0],
                date=self.selected_date,
                amount=self.amount,
                doc_sn=self.document_serial_number,
            )
            self.transaction_id = txns.json()[0]["id"]
            self.saved = True
        else:
            st.error("Completați toate câmpurile")

    def render(self):
        with st.container(border=True):
            st.header("Creează o tranzacție dintr-un șablon")
            self.available_templates = st.session_state.available_templates

            self.selected_date = st.date_input(
                "Data", key=self.unique_id + "date"
            ).strftime("%Y-%m-%d")

            self.amount = st.number_input(
                "Suma", self.amount, key=self.unique_id + "amount"
            )

            self.selected_template = st.selectbox(
                "Șablon",
                self.available_templates["name"],
                key=self.unique_id + "template",
            )

            document_details = st.checkbox("Detalii document justificativ")
            if document_details:
                self.document_serial_number = st.text_input(
                    "Serie document justificativ"
                )

            main_transaction = self.available_templates.loc[
                self.available_templates["name"] == self.selected_template,
                "main_transaction",
            ].iloc[0]

            self.main_transaction_card = TransactionCard(
                debit_account=main_transaction["debit_account"],
                credit_account=main_transaction["credit_account"],
                details=main_transaction["details"],
                date=self.selected_date,
                currency=main_transaction["currency"],
                amount=self.amount,
            )

            self.main_transaction_card.render()

            for transaction in self.available_templates.loc[
                self.available_templates["name"] == self.selected_template,
                "followup_transactions",
            ].iloc[0]:
                TransactionCard(
                    debit_account=transaction["debit_account"],
                    credit_account=transaction["credit_account"],
                    details=transaction["details"],
                    date=self.selected_date,
                    currency=main_transaction["currency"],
                    amount=self.amount,
                    operation=transaction["operation"],
                ).render()
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                if self.saved:
                    st.success("Tranzacție salvată")
                else:
                    st.button(
                        "Salvează tranzacțiile",
                        key=self.unique_id + "sv",
                        on_click=self.save,
                    )
            with c4:
                st.button(
                    "Resetează formularul",
                    key=self.unique_id + "rst",
                    on_click=lambda: self.__init__(),
                )
