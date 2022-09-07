from src.main.config import db
from src.infra.persistence.sqlalchemy.models import Category


class UpdateCategoryRepository:
    def handle(self, _id: str, name: str, parent_id: str):
        category = Category.query.get(_id)
        category.name = name
        category.parent_id = parent_id
        db.session.add(category)
        db.session.commit()
        return category
