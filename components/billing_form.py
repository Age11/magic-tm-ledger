import uuid
import streamlit as st
from components.dataframe_with_selection import dataframe_with_selections
from components.invoice_payment_card import InvoicePaymentCard


class BillingForm:
    def __init__(self):
        self.unique_id = None
        self.data = []
        self.unique_id = "billing_form" + uuid.uuid4().hex
        self.payment_cards = []

    def render(self):
        for payment in self.data:
            found = False
            for card in self.payment_cards:
                if card.payment["id"] == payment["id"]:
                    found = True
            if not found:
                self.payment_cards.append(InvoicePaymentCard(payment))

        for card in self.payment_cards:
            card.render()
