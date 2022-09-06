from flask import current_app

from src.main.routes import categories, expenses


def create_routes(app: current_app):
    app.register_blueprint(categories)
    app.register_blueprint(expenses)
