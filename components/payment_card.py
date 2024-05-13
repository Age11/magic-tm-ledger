import uuid
from datetime import datetime
import streamlit as st


class PaymentCard:
    def __init__(self, payment):
        self.payment = payment
        self.available_templates = st.session_state.available_templates
        self.unique_id = uuid.uuid4().hex
        self.saved = False
        self.amount_to_pay = payment["amount_due"]
        self.installment_type = None

    def save_payment(self):
        st.session_state.api_client.payments.solve_payment(self.payment["id"], self.amount_to_pay, self.installment_type)
        st.session_state.api_client.transactions.create_transaction_from_template(
            self.selected_template_id,
            self.amount_to_pay,
            self.payment["due_date"],
        )
        st.session_state.receivable_billing_form.clear_payment_cards()
        st.session_state.payable_billing_form.clear_payment_cards()

    def render(self):
        with st.container(border=True):
            st.write(f"Generată de: {self.payment["details"]}")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.write("Plata:")
                st.write(f"Id-{self.payment["id"]}")
            with c2:
                st.write("Scadența:")
                st.write(self.payment["due_date"])
            with c3:
                st.write("Stare:")
                st.write(self.payment["payment_status"])
            with c4:
                st.write("De plată:")
                st.write(f"{self.payment["pending_amount"]} {self.payment["currency"]}")

            c5, c6 = st.columns(2)
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

                sc1, sc2 = st.columns(2)
                with sc1:
                    self.amount_to_pay = st.number_input("Sumă", key=self.unique_id + "amount")
                with sc2:
                    if self.amount_to_pay <= self.payment["amount_due"]:
                        self.installment_type = st.selectbox(
                            "Tipul plății",
                            [ "bancă", "casă"],
                            index=0,
                            key=self.unique_id + "installment_type",
                        )
                        st.button("Procesează", key=self.unique_id + str(self.payment["id"]), on_click=self.save_payment)
                    else:
                        st.warning("Suma introdusă este mai mare decât suma de plată!")