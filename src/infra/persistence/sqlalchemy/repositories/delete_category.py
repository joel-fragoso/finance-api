from src.main.config import db
from src.infra.persistence.sqlalchemy.models import Category


class DeleteCategoryRepository:
    def handle(self, category_id: str):
        category = Category.query.get(category_id)
        db.session.delete(category)
        db.session.commit()
        return category
