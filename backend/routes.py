"""
routes.py – HTTP endpoints for the Employee-Directory API
---------------------------------------------------------
• JWT required on every /employees call
• created_by recorded on POST
• /login returns expires_in
• /healthz probe
"""

from datetime import timedelta

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from sqlalchemy import or_

from models import db, Employee, User

api = Blueprint("api", __name__, url_prefix="/api")


# ────────────────────────── helpers ────────────────────────────
def _missing(*fields):
    return {"msg": f"Missing required fields: {', '.join(fields)}"}, 400


# ───────────────────────── auth ────────────────────────────────
@api.post("/register")                      # ⛔ remove or harden in prod
def register():
    data = request.get_json(silent=True) or {}
    if not all(k in data for k in ("username", "password")):
        return _missing("username", "password")

    if User.query.filter_by(username=data["username"]).first():
        return {"msg": "User already exists"}, 409

    user = User(username=data["username"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return {"msg": "registered"}, 201


@api.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    if not all(k in data for k in ("username", "password")):
        return _missing("username", "password")

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
        return {"msg": "Bad credentials"}, 401

    expires = timedelta(hours=1)
    # PyJWT requires the "sub" claim (identity) to be a STRING
    token = create_access_token(identity=str(user.id), expires_delta=expires)
    return {"access_token": token, "expires_in": expires.seconds}, 200


# ─────────────────────── employees ─────────────────────────────
@api.get("/employees")
@jwt_required()
def list_or_search():
    q = request.args.get("q") or request.args.get("search")
    query = Employee.query
    if q:
        ilike = f"%{q}%"
        query = query.filter(or_(Employee.name.ilike(ilike),
                                 Employee.department.ilike(ilike)))
    return jsonify([e.to_dict() for e in query.all()])


@api.post("/employees")
@jwt_required()
def add_employee():
    data = request.get_json(silent=True) or {}
    if not all(k in data for k in ("name", "department")):
        return _missing("name", "department")

    emp = Employee(
        name=data["name"],
        department=data["department"],
        created_by=int(get_jwt_identity())   # ← str → int
    )
    db.session.add(emp)
    db.session.commit()
    return emp.to_dict(), 201


@api.put("/employees/<int:emp_id>")
@jwt_required()
def update_employee(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    data = request.get_json(silent=True) or {}
    if not data:
        return {"msg": "Nothing to update"}, 400

    emp.name       = data.get("name", emp.name)
    emp.department = data.get("department", emp.department)
    db.session.commit()
    return emp.to_dict(), 200


@api.delete("/employees/<int:emp_id>")
@jwt_required()
def delete_employee(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    db.session.delete(emp)
    db.session.commit()
    return {"msg": "deleted"}, 200


# ─────────────────────── health probe ──────────────────────────
@api.get("/healthz")
def health():
    return {"status": "ok"}, 200