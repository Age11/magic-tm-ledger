import streamlit as st

from account_plan import account_plan


class TransactionCard:
    def __init__(
        self,
        debit_account,
        credit_account,
        details,
        date,
        amount,
        currency,
        operation=None,
    ):
        self.debit_account = debit_account
        self.credit_account = credit_account
        self.details = details
        self.date = date
        self.amount = amount
        self.currency = currency
        self.operation = operation

    def render(self):
        with st.container(border=True):
            st.write(f"{self.details} {self.date}")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(self.debit_account)
                debit_name = account_plan.get(self.debit_account)
                if debit_name is not None:
                    with st.expander("denumire cont", expanded=False):
                        st.write(debit_name)
            with col2:
                st.write("=")
            with col3:
                st.write(self.credit_account)
                credit_name = account_plan.get(self.credit_account)
                if credit_name is not None:
                    with st.expander("denumire cont", expanded=False):
                        st.write(credit_name)
            with col4:
                if self.operation is not None:
                    self.amount = eval(str(self.amount) + self.operation)
                st.write(f"{self.amount} {self.currency}")
