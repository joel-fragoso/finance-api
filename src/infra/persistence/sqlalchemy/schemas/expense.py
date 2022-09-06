from flask_marshmallow.fields import fields

from src.main.config import ma
from src.infra.persistence.sqlalchemy.models import Expense
from src.infra.persistence.sqlalchemy.schemas import CategorySchema


class ExpenseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Expense

    amount = fields.Number()
    category = fields.Nested(CategorySchema)


expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)
