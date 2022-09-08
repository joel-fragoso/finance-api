from src.main.config import db
from src.infra.persistence.sqlalchemy.models import Expense


class DeleteExpenseRepository:
    def handle(self, expense_id: str):
        expense = Expense.query.get(expense_id)
        db.session.delete(expense)
        db.session.commit()
        return expense
