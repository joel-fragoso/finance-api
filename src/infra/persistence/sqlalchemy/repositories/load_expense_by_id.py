from src.infra.persistence.sqlalchemy.models import Expense


class LoadExpenseByIdRepository:
    def handle(self, expense_id: str):
        expense = Expense.query.get(expense_id)
        return expense
