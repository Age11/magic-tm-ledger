import streamlit as st

from api_client.invoices import create_invoice


class InflowInvoiceForm:
    def __init__(self, unique_id, project_id, suppliers, client):
        self.unique_id = unique_id
        self.suppliers = suppliers
        self.client = client
        self.saved = False
        self.updated = False
        self.project_id = project_id
        self.invoice_id = None

        self.serial_number = None
        self.invoice_date = None
        self.due_date = None
        self.supplier = None
        self.client = client
        self.currency = None
        self.amount = None
        self.vat_amount = None
        self.issuer_name = None

    def to_dict(self):
        data_dict = {
            "serial_number": self.serial_number,
            "invoice_date": self.invoice_date.strftime("%Y-%m-%d"),
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "supplier_id": int(self.supplier),
            "client_id": int(self.client),
            "currency": self.currency,
            "amount": round(float(self.amount), 2),
            "vat_amount": round(float(self.vat_amount), 2),
            "issuer_name": self.issuer_name,
        }

        for key, value in data_dict.items():
            print(f"{key}: {type(value)}")

        return data_dict

    def render(self):
        with st.container():
            self.serial_number = st.text_input(
                "Seria", self.serial_number, key=self.unique_id + "serial-number"
            )
            self.invoice_date = st.date_input(
                "Data facturii", key=self.unique_id + "invoice-date"
            )
            self.due_date = st.date_input(
                "Data scadenței", key=self.unique_id + "due-date"
            )
            user_selection = st.selectbox(
                "Furnizor",
                self.suppliers["organization_name"],
                index=0,
            )
            self.supplier = self.suppliers[
                self.suppliers["organization_name"] == user_selection
            ]["id"].iloc[0]

            self.currency = st.selectbox(
                "Moneda", ["RON", "EUR"], key=self.unique_id + "currency"
            )
            self.amount = st.number_input("Suma", key=self.unique_id + "amount")

            self.vat_amount = st.number_input(
                "Suma TVA", key=self.unique_id + "vat-amount"
            )

            self.issuer_name = st.text_input(
                "Nume Emitent", key=self.unique_id + "issuer-name"
            )

            if not self.saved:
                if st.button("Salvează", key=self.unique_id + "save"):
                    if all(
                        [
                            self.serial_number,
                            self.invoice_date,
                            self.due_date,
                            self.supplier,
                            self.client,
                            self.currency,
                            self.amount,
                            self.vat_amount,
                            self.issuer_name,
                        ]
                    ):
                        self.saved = True
                        self.invoice_id = create_invoice(
                            self.project_id, self.to_dict()
                        )

                    else:
                        st.error("Toate câmpurile sunt obligatorii")
            else:
                if st.button("Actualizează", key=self.unique_id + "update"):
                    if all(
                        [
                            self.serial_number,
                            self.invoice_date,
                            self.due_date,
                            self.supplier,
                            self.client,
                            self.currency,
                            self.amount,
                            self.issuer_name,
                        ]
                    ):
                        self.updated = True
                        print(self.to_dict())
                    else:
                        st.error("Toate câmpurile sunt obligatorii")
            if self.saved and not self.updated:
                st.success("Factura a fost salvată")
            elif self.updated:
                st.success("Factura a fost actualizată")
