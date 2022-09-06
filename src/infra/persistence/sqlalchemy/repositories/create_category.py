from src.main.config import db
from src.infra.persistence.sqlalchemy.models import Category


class CreateCategoryRepository:
    def handle(self, _id, name, parent_id):
        category = Category(_id=_id, name=name, parent_id=parent_id)
        db.session.add(category)
        db.session.commit()
        return category
