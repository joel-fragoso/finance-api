from src.main.config import db
from src.infra.persistence.sqlalchemy.models import Expense


class UpdateExpenseRepository:
    def handle(self, expense_id: str, amount: float, category_id: str):
        expense = Expense.query.get(expense_id)
        expense.amount = amount
        expense.category_id = category_id
        db.session.add(expense)
        db.session.commit()
        return expense
