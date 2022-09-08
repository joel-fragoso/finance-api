import uuid
from flask import Blueprint, Response, request, jsonify

from src.main.config import db
from src.infra.persistence.sqlalchemy.schemas import expense_schema, expenses_schema
from src.infra.persistence.sqlalchemy.repositories import (
    CreateExpenseRepository,
    DeleteExpenseRepository,
    LoadExpensesRepository,
    LoadExpenseByIdRepository,
    UpdateExpenseRepository,
)

expenses = Blueprint("expenses", __name__, url_prefix="/api/v1.0")


@expenses.get("/expenses")
def expenses_index() -> Response:
    try:
        expenses_entity = LoadExpensesRepository().handle()
        return jsonify(expenses_schema.dump(expenses_entity)), 200
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400


@expenses.get("/expenses/<_id>")
def expenses_show(_id: str) -> Response:
    try:
        expense_entity = LoadExpenseByIdRepository().handle(expense_id=_id)
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
        expense_entity = CreateExpenseRepository().handle(
            expense_id=str(uuid.uuid4()),
            amount=amount,
            category_id=category_id,
        )
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
        expense_entity = UpdateExpenseRepository().handle(
            expense_id=_id, amount=amount, category_id=category_id
        )
        return expense_schema.jsonify(expense_entity), 200
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400


@expenses.delete("/expenses/<_id>")
def expenses_delete(_id: str) -> Response:
    try:
        expense_entity = DeleteExpenseRepository().handle(expense_id=_id)
        return expense_schema.jsonify(expense_entity), 204
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400
