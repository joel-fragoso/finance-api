from src.infra.persistence.sqlalchemy.models import Expense


class LoadExpensesRepository:
    def handle(self):
        expenses = Expense.query.all()
        return expenses
