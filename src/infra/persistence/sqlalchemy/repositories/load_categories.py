from src.infra.persistence.sqlalchemy.models import Category


class LoadCategoriesRepository:
    def handle(self):
        categories = Category.query.all()
        return categories
