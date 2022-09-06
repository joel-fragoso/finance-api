from datetime import datetime

from src.main.config import db


class Expense(db.Model):
    __tablename__ = "expenses"
    _id = db.Column("id", db.String(36), primary_key=True, autoincrement=False)
    amount = db.Column("amount", db.Numeric(10, 2), nullable=False)
    created_at = db.Column(
        "created_at", db.DateTime(), nullable=False, default=datetime.utcnow
    )
    updated_at = db.Column(
        "updated_at",
        db.DateTime(),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    category_id = db.Column(
        db.String(36), db.ForeignKey("categories.id"), nullable=False
    )
    category = db.relationship("Category", backref="expenses", lazy="subquery")

    def __init__(
        self,
        _id: str,
        amount: float,
        category_id: str,
    ) -> None:
        self._id = _id
        self.amount = amount
        self.category_id = category_id
