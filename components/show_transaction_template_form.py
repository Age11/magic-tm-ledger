import uuid

import streamlit as st

from components.transaction_card import TransactionCard


class ShowTemplateForm:

    def __init__(self, available_templates, date, amount, doc_sn, doc_id):
        self.available_templates = available_templates
        self.unique_id = uuid.uuid4().hex
        self.date = date
        self.amount = amount
        self.doc_sn = doc_sn
        self.doc_id = doc_id

    def save(self):
        st.session_state.api_client.transactions.create_transaction_from_template(
            transaction_template_id=self.selected_template_id,
            amount=self.amount,
            date=self.date,
            doc_sn=self.doc_sn,
            doc_id=self.doc_id,
        )

    def render(self):
        selected_template = st.selectbox(
            "Șablon",
            self.available_templates["name"],
            key=self.unique_id + "template",
            index=0,
        )

        self.selected_template_id = (
            self.available_templates.loc[
                self.available_templates["name"] == selected_template,
                "id",
            ].iloc[0],
        )[0]

        main_transaction = self.available_templates.loc[
            self.available_templates["name"] == selected_template,
            "main_transaction",
        ].iloc[0]

        main_transaction_card = TransactionCard(
            debit_account=main_transaction["debit_account"],
            credit_account=main_transaction["credit_account"],
            details=main_transaction["details"],
            date=self.date,
            currency=main_transaction["currency"],
            amount=self.amount,
        )

        main_transaction_card.render()

        for transaction in self.available_templates.loc[
            self.available_templates["name"] == selected_template,
            "followup_transactions",
        ].iloc[0]:
            TransactionCard(
                debit_account=transaction["debit_account"],
                credit_account=transaction["credit_account"],
                details=transaction["details"],
                date=self.date,
                currency=main_transaction["currency"],
                amount=self.amount,
                operation=transaction["operation"],
            ).render()
