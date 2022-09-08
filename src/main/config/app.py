from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from .env import Config

db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        from src.main.config import create_routes

        create_routes(app)
        return app
