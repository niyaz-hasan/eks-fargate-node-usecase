from flask import Blueprint, jsonify, request
from models import db, Employee

api = Blueprint('api', __name__)

@api.route('/api/employees', methods=['GET'])
def list_employees():
    return jsonify([e.to_dict() for e in Employee.query.all()])

@api.route('/api/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    emp = Employee(name=data['name'], department=data['department'])
    db.session.add(emp)
    db.session.commit()
    return jsonify(emp.to_dict()), 201