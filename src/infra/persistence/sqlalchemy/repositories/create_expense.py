from src.main.config import db
from src.infra.persistence.sqlalchemy.models import Expense


class CreateExpenseRepository:
    def handle(self, expense_id: str, amount: float, category_id: str):
        expense = Expense(_id=expense_id, amount=amount, category_id=category_id)
        db.session.add(expense)
        db.session.commit()
        return expense
