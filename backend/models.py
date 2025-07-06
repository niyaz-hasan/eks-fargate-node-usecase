"""
models.py  –  single source of truth for SQLAlchemy models
----------------------------------------------------------

• Removes duplicate class definitions that caused
  `InvalidRequestError: Table 'user' is already defined…`.
• Adds __tablename__ and __table_args__ with extend_existing=True
  to make re-imports idempotent.
• Keeps created_by → User.id foreign key and a back-reference.
"""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# ─────────────────────────────  User  ────────────────────────────────────────
class User(db.Model):
    __tablename__ = "user"                     # explicit name
    __table_args__ = {"extend_existing": True}  # safe re-import

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _pw_hash = db.Column("password", db.String(255), nullable=False)

    # Relationship (one user → many employees)
    employees = db.relationship("Employee", backref="creator", lazy=True)

    # Helpers ­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­
    def set_password(self, plaintext: str) -> None:
        self._pw_hash = generate_password_hash(plaintext)

    def check_password(self, plaintext: str) -> bool:
        return check_password_hash(self._pw_hash, plaintext)

    def to_dict(self) -> dict:
        return {"id": self.id, "username": self.username}


# ────────────────────────────  Employee  ─────────────────────────────────────
class Employee(db.Model):
    __tablename__ = "employee"
    __table_args__ = {"extend_existing": True}

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(80), nullable=False)
    department  = db.Column(db.String(80), nullable=False)
    created_by  = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
        }
