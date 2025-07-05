from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models import db, Employee
from werkzeug.security import generate_password_hash, check_password_hash

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # In a real app, you would verify credentials against a user database
    # This is a simplified example
    if email == 'admin@company.com' and password == 'password':
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad credentials"}), 401

@api_blueprint.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    search = request.args.get('search', '')
    query = Employee.query
    
    if search:
        query = query.filter(
            (Employee.name.ilike(f'%{search}%')) | 
            (Employee.department.ilike(f'%{search}%'))
        )
    
    employees = query.all()
    return jsonify([employee.to_dict() for employee in employees])

@api_blueprint.route('/employees/<int:employee_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    current_user = get_jwt_identity()
    employee = Employee.query.get_or_404(employee_id)
    
    # In a real app, you would verify the user can only update their own record
    data = request.get_json()
    
    employee.name = data.get('name', employee.name)
    employee.email = data.get('email', employee.email)
    employee.department = data.get('department', employee.department)
    employee.phone = data.get('phone', employee.phone)
    
    db.session.commit()
    return jsonify(employee.to_dict())

@api_blueprint.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200