from src.infra.persistence.sqlalchemy.models import Category


class LoadCategoryByIdRepository:
    def handle(self, category_id: str):
        category = Category.query.get(category_id)
        return category
