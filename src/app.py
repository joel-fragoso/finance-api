import os
from flask import Blueprint, Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from .sqlalchemy_mysql_binary_uuid import BinaryUUID

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv(
    "SQLALCHEMY_TRACK_MODIFICATIONS"
)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

db = SQLAlchemy(app)


class Category(db.Model):
    __tablename__ = "categories"
    # pylint: disable=no-member
    id = db.Column("id", BinaryUUID, primary_key=True, autoincrement=False)
    name = db.Column("name", db.String(45), unique=True, nullable=False)

    def __repr__(self):
        return f"<Category: {self.name}"


categories = Blueprint("categories", __name__)


@categories.get("/categories")
def index():
    return jsonify(message="Bem vindo!"), 200


app.register_blueprint(categories, url_prefix="/api/v1.0")

if __name__ == "__main__":
    app.run()
