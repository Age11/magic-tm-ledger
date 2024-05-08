import uuid

import pandas as pd
import streamlit as st

from api_client.transaction import (
    fetch_transaction_templates,
    create_transaction_from_template,
)
from components.transaction_card import TransactionCard


class TransactionFromTemplateForm:
    def __init__(self):
        self.unique_id = uuid.uuid4().hex
        self.amount = None
        self.available_templates = None

    def render(self):
        with st.container(border=True):
            st.header("Creează o tranzacție dintr-un șablon")
            self.available_templates = pd.DataFrame(
                fetch_transaction_templates(st.session_state.selected_project["id"])
            )

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
                document_serial_number = st.text_input("Serie document justificativ")
                document_details = st.text_area("Detalii document justificativ")
                document_type = st.selectbox(
                    "Tip document justificativ",
                    [
                        "Factură",
                        "Chitanțe",
                        "Proces-verbal",
                        "Ordin de plată",
                        "Contract",
                        "Declarație bancară",
                        "Ștat de salarii",
                        "Notă contabilă",
                        "Bilet la ordin",
                    ],
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

            if st.button("Salvează tranzacțiile"):
                print(self.selected_template)
                create_transaction_from_template(
                    project_id=st.session_state["selected_project"]["id"],
                    transaction_template_id=self.available_templates.loc[
                        self.available_templates["name"] == self.selected_template,
                        "id",
                    ].iloc[0],
                    date=self.selected_date,
                    amount=self.amount,
                )
