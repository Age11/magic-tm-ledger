import uuid

import streamlit as st
from account_plan import account_plan
from api_client.transaction import create_transaction
from components.create_payment_form import CreatePaymentForm


class TransactionForm:

    def __init__(self):
        self.unique_id = uuid.uuid4().hex
        self.debit_account = None
        self.credit_account = None
        self.debit_amount = None
        self.credit_amount = None
        self.currency = None
        self.transaction_date = None
        self.details = None
        self.tx_type = None

        self.document_serial_number = "N/A"
        self.document_type = "N/A"

        self.create_payment_form = None

        self.saved = False
        self.transaction = None
        self.payment_details = False

        self.document_details = False

    def to_dict(self):
        return {
            "debit_account": self.debit_account,
            "credit_account": self.credit_account,
            "debit_amount": round(float(self.debit_amount), 2),
            "credit_amount": round(float(self.credit_amount), 2),
            "currency": self.currency,
            "transaction_date": self.transaction_date.strftime("%Y-%m-%d"),
            "details": self.details,
            "tx_type": self.tx_type,
            "document_serial_number": self.document_serial_number,
            "document_type": self.document_type,
        }

    def save(self):
        if all(
            [
                self.debit_account,
                self.credit_account,
                self.debit_amount,
                self.currency,
                self.transaction_date,
                self.tx_type,
                self.details,
                self.document_serial_number,
                self.document_type,
            ]
        ):
            print("Tranzacție salvată")
            st.session_state["created_tx_id"] = (
                create_transaction(
                    project_id=st.session_state["selected_project"]["id"],
                    transaction_data=self.to_dict(),
                )
                .headers["location"]
                .split("/")[-1]
            )
            self.saved = True
        else:
            st.error("Completează toate câmpurile")

    def reset(self):
        self.__init__()
        st.session_state["tx_create_payment_form"] = []
        print("tried to reset")

    def render(self):
        with st.container(border=True):
            st.header("Creează o tranzacție")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                self.debit_account = st.text_input(
                    "Cont debitor",
                    self.debit_account,
                    key=self.unique_id + "debtor_account",
                )
                account_name = account_plan.get(self.debit_account)
                if account_name is not None:
                    with st.expander("denumire cont", expanded=False):
                        st.write(account_name)
            with col2:
                c1, c2, c3 = st.columns(3)
                with c2:
                    st.header("🟰")
            with col3:
                self.credit_account = st.text_input(
                    "Cont creditor",
                    self.credit_account,
                    key=self.unique_id + "creditor_account",
                )
                account_name = account_plan.get(self.credit_account)
                if account_name is not None:
                    with st.expander("denumire cont", expanded=False):
                        st.write(account_name)
            with col4:
                self.debit_amount = st.number_input(
                    "Suma", self.debit_amount, key=self.unique_id + "debtor_amount"
                )
                self.credit_amount = self.debit_amount

            self.currency = st.selectbox("Moneda", ["RON", "EUR"], index=0)
            self.transaction_date = st.date_input(
                "Data tranzacției",
                self.transaction_date,
                key=self.unique_id + "transaction_date",
            )
            self.tx_type = st.selectbox(
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

            self.details = st.text_area(
                "Detalii", self.details, key=self.unique_id + "details"
            )

            self.document_details = st.checkbox("Detalii document justificativ")
            if self.document_details:
                self.document_serial_number = st.text_input(
                    "Serie document justificativ"
                )
                self.document_type = st.selectbox(
                    "Tip document justificativ",
                    [
                        "factură",
                        "ștat de plată",
                        "proces-verbal",
                        "OP",
                        "contract",
                        "notă contabilă",
                        "bilet la ordin",
                        "chitanță",
                        "declarație bancară",
                        "bon de consum",
                        "extras bancar",
                    ],
                    index=0,
                    key=self.unique_id + "document_type",
                )

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                if self.saved:
                    st.success("Tranzacție salvată")
                    payment_details = st.checkbox("Adaugă detalii de plată")
                    if payment_details:
                        if "tx_create_payment_form" not in st.session_state.keys():

                            st.session_state["tx_create_payment_form"] = []
                            print("Create the thig")
                        if (
                            "created_tx_id" in st.session_state.keys()
                            and len(st.session_state["tx_create_payment_form"]) == 0
                        ):
                            st.session_state["tx_create_payment_form"].append(
                                CreatePaymentForm(
                                    transaction_id=st.session_state.created_tx_id
                                )
                            )
                            print("added foooorm")

                else:
                    st.button(
                        "Salvează",
                        key=self.unique_id + "svbtn",
                        on_click=lambda: self.save(),
                    )

            with c4:
                st.button(
                    "Resetează formular",
                    key=self.unique_id + "rstbtn",
                    on_click=lambda: self.reset(),
                )

            if "tx_create_payment_form" in st.session_state.keys():
                print("should fucking render")
                for form in st.session_state.tx_create_payment_form:
                    form.render()
