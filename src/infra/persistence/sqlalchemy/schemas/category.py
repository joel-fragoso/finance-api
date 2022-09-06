from flask_marshmallow.fields import fields

from src.main.config import ma
from src.infra.persistence.sqlalchemy.models import Category


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category

    children = fields.Nested("self", many=True)


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
