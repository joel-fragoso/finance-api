from src.main.config import db
from src.infra.persistence.sqlalchemy.models import Category


class UpdateCategoryRepository:
    def handle(self, category_id: str, name: str, parent_id: str):
        category = Category.query.get(category_id)
        category.name = name
        category.parent_id = parent_id
        db.session.add(category)
        db.session.commit()
        return category
