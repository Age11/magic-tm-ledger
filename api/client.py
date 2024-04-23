from api.account_balance import AccountBalance
from api.inventories import Inventories
from api.invoices import Invoices
from api.projects import Projects
from api.reports import Reports
from api.third_parties import ThirdParties
from api.transactions import Transactions


class Client:
    def __init__(self, project_id):
        self.inventories = Inventories(project_id)
        self.invoices = Invoices(project_id)
        self.reports = Reports(project_id)
        self.transactions = Transactions(project_id)
        self.third_parties = ThirdParties(project_id)
        self.projects = Projects(project_id)
        self.account_balance = AccountBalance(project_id)
