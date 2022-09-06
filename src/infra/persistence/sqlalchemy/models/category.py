from datetime import datetime
from typing import Optional

from src.main.config import db


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
