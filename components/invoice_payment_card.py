import uuid
from datetime import datetime
import streamlit as st


class InvoicePaymentCard:
    def __init__(self, payment):
        self.payment = payment
        self.available_templates = st.session_state.available_templates
        self.unique_id = uuid.uuid4().hex
        self.saved = False

    def save_payment(self):
        st.session_state.api_client.invoices.solve_payment(self.payment["id"])
        st.session_state.api_client.transactions.create_transaction_from_template(
            self.selected_template_id,
            self.payment["total_amount"],
            self.payment["due_date"],
        )
        self.saved = True

    def render(self):
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.write("Factura:")
                st.write(self.payment["serial_number"])
            with c2:
                st.write("Scadența:")
                st.write(self.payment["due_date"])
            with c3:
                st.write("Stare:")
                st.write(self.payment["payment_status"])
            with c4:
                st.write("Total:")
                st.write(f"{self.payment["total_amount"]} {self.payment["currency"]}")

            c5, c6, = st.columns(2)
            with c5:
                selected_template = st.selectbox(
                    "Șablon",
                    self.available_templates["name"],
                    key=self.unique_id + "template",
                    index=0,
                )
                self.selected_template_id = (
                    self.available_templates.loc[
                        st.session_state.available_templates["name"]
                        == selected_template,
                        "id",
                    ].iloc[0],
                )[0]
            with c6:
                if not self.saved:
                    st.write("")
                    st.write("")
                    st.button("Procesează", key=self.unique_id + self.payment["serial_number"], on_click=self.save_payment)
                else:
                    st.write("")
                    st.write("")
                    st.write("Procesare efectuată!")