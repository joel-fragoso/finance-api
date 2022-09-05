import os
import uuid
from typing import Optional
from datetime import datetime
from flask import Blueprint, Flask, jsonify, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv(
    "SQLALCHEMY_TRACK_MODIFICATIONS"
)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Category(db.Model):
    __tablename__ = "categories"
    _id = db.Column("id", db.String(36), primary_key=True, autoincrement=False)
    name = db.Column("name", db.String(45), unique=True, nullable=False)
    created_at = db.Column(
        "created_at", db.DateTime(), nullable=False, default=datetime.utcnow
    )
    updated_at = db.Column(
        "updated_at",
        db.DateTime(),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    parent_id = db.Column(db.String(36), db.ForeignKey("categories.id"))
    children = db.relationship("Category")

    def __init__(self, _id: str, name: str, parent_id: Optional[str] = None) -> None:
        self._id = _id
        self.name = name
        self.parent_id = parent_id


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category

    children = fields.Nested("self", many=True)


class Expense(db.Model):
    __tablename__ = "expenses"
    _id = db.Column("id", db.String(36), primary_key=True, autoincrement=False)
    amount = db.Column("amount", db.Numeric(10, 2), nullable=False)
    created_at = db.Column(
        "created_at", db.DateTime(), nullable=False, default=datetime.utcnow
    )
    updated_at = db.Column(
        "updated_at",
        db.DateTime(),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    category_id = db.Column(
        db.String(36), db.ForeignKey("categories.id"), nullable=False
    )
    category = db.relationship("Category", backref="expenses", lazy="subquery")

    def __init__(
        self,
        _id: str,
        amount: float,
        category_id: str,
    ) -> None:
        self._id = _id
        self.amount = amount
        self.category_id = category_id


class ExpenseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Expense

    amount = fields.Number()
    category = fields.Nested(CategorySchema)


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)

welcome = Blueprint("welcome", __name__)


@welcome.get("/")
def welcome_index() -> Response:
    return jsonify(body="Bem vindo!"), 200


categories = Blueprint("categories", __name__)


@categories.get("/categories")
def categories_index() -> Response:
    try:
        categories_entity = Category.query.all()
        return jsonify(categories_schema.dump(categories_entity)), 200
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400


@categories.get("/categories/<_id>")
def categories_show(_id: str) -> Response:
    try:
        category_entity = Category.query.get(_id)
        return category_schema.jsonify(category_entity), 200
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400


@categories.post("/categories")
def categories_create() -> Response:
    name = request.json.get("name", "")
    parent_id = request.json.get("parent_id", None)
    try:
        category_entity = Category(
            _id=str(uuid.uuid4()), name=name, parent_id=parent_id
        )
        db.session.add(category_entity)
        db.session.commit()
        return category_schema.jsonify(category_entity), 201
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400


@categories.put("/categories/<_id>")
def categories_update(_id: str) -> Response:
    name = request.json.get("name", "")
    parent_id = request.json.get("parent_id", None)
    try:
        category_entity = Category.query.get(_id)
        category_entity.name = name
        category_entity.parent_id = parent_id
        db.session.add(category_entity)
        db.session.commit()
        return category_schema.jsonify(category_entity), 200
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400


@categories.delete("/categories/<_id>")
def categories_delete(_id: str) -> Response:
    try:
        category_entity = Category.query.get(_id)
        db.session.delete(category_entity)
        db.session.commit()
        return category_schema.jsonify(category_entity), 204
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400


expenses = Blueprint("expenses", __name__)


@expenses.get("/expenses")
def expenses_index() -> Response:
    try:
        expenses_entity = Expense.query.all()
        return jsonify(expenses_schema.dump(expenses_entity)), 200
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400


@expenses.get("/expenses/<_id>")
def expenses_show(_id: str) -> Response:
    try:
        expense_entity = Expense.query.get(_id)
        return expense_schema.jsonify(expense_entity), 200
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400


@expenses.post("/expenses")
def expenses_create() -> Response:
    category_id = request.json.get("category_id", "")
    amount = request.json.get("amount", "")
    try:
        expense_entity = Expense(
            _id=str(uuid.uuid4()),
            amount=amount,
            category_id=category_id,
        )
        db.session.add(expense_entity)
        db.session.commit()
        return expense_schema.jsonify(expense_entity), 201
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400


@expenses.put("/expenses/<_id>")
def expenses_update(_id: str) -> Response:
    category_id = request.json.get("category_id", "")
    amount = request.json.get("amount", "")
    try:
        expense_entity = Expense.query.get(_id)
        expense_entity.category_id = category_id
        expense_entity.amount = amount
        db.session.add(expense_entity)
        db.session.commit()
        return expense_schema.jsonify(expense_entity), 200
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400


@expenses.delete("/expenses/<_id>")
def expenses_delete(_id: str) -> Response:
    try:
        expense_entity = Expense.query.get(_id)
        db.session.delete(expense_entity)
        db.session.commit()
        return expense_schema.jsonify(expense_entity), 204
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400


app.register_blueprint(welcome)
app.register_blueprint(categories, url_prefix="/api/v1.0")
app.register_blueprint(expenses, url_prefix="/api/v1.0")

if __name__ == "__main__":
    app.run(debug=True)
