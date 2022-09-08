import uuid
from flask import Blueprint, Response, request, jsonify

from src.main.config import db
from src.infra.persistence.sqlalchemy.schemas import category_schema, categories_schema
from src.infra.persistence.sqlalchemy.repositories import (
    CreateCategoryRepository,
    DeleteCategoryRepository,
    LoadCategoriesRepository,
    LoadCategoryByIdRepository,
    UpdateCategoryRepository,
)

categories = Blueprint("categories", __name__, url_prefix="/api/v1.0")


@categories.get("/categories")
def index() -> Response:
    try:
        categories_entity = LoadCategoriesRepository().handle()
        return jsonify(categories_schema.dump(categories_entity)), 200
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400


@categories.get("/categories/<_id>")
def show(_id: str) -> Response:
    try:
        category_entity = LoadCategoryByIdRepository().handle(category_id=_id)
        return category_schema.jsonify(category_entity), 200
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400


@categories.post("/categories")
def create() -> Response:
    name = request.json.get("name", "")
    parent_id = request.json.get("parent_id", None)
    try:
        category_entity = CreateCategoryRepository().handle(
            _id=str(uuid.uuid4()), name=name, parent_id=parent_id
        )
        return category_schema.jsonify(category_entity), 201
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400


@categories.put("/categories/<_id>")
def update(_id: str) -> Response:
    name = request.json.get("name", "")
    parent_id = request.json.get("parent_id", None)
    try:
        category_entity = UpdateCategoryRepository().handle(
            category_id=_id, name=name, parent_id=parent_id
        )
        return category_schema.jsonify(category_entity), 200
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400


@categories.delete("/categories/<_id>")
def delete(_id: str) -> Response:
    try:
        category_entity = DeleteCategoryRepository().handle(category_id=_id)
        return category_schema.jsonify(category_entity), 204
    except TypeError as error:
        print(error)
        db.session.rollback()
        return jsonify(status_code=400, body="Bad Request."), 400
