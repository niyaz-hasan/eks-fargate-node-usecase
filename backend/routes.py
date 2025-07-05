from flask import Blueprint, request, jsonify
from models import db, Employee
import jwt
from functools import wraps
import datetime
from flask import current_app

main = Blueprint('main', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Employee.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@main.route('/api/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify'}), 401

    user = Employee.query.filter_by(email=auth.username).first()

    if not user or not user.check_password(auth.password):
        return jsonify({'message': 'Could not verify'}), 401
    
    token = jwt.encode({'id': user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
    
    return jsonify({'token' : token})

@main.route('/api/employees', methods=['GET'])
@token_required
def get_employees(current_user):
    name = request.args.get('name')
    department = request.args.get('department')
    
    query = Employee.query
    if name:
        query = query.filter(Employee.name.ilike(f'%{name}%'))
    if department:
        query = query.filter(Employee.department.ilike(f'%{department}%'))
        
    employees = query.all()
    return jsonify([e.to_dict() for e in employees])

@main.route('/api/employees/<int:id>', methods=['PUT'])
@token_required
def update_employee(current_user, id):
    if current_user.id != id:
        return jsonify({'message': 'Cannot update another user'}), 403
        
    data = request.get_json()
    employee = Employee.query.get_or_404(id)
    
    employee.phone = data.get('phone', employee.phone)
    # Add other updatable fields as necessary
    
    db.session.commit()
    return jsonify(employee.to_dict())

@main.route('/api/employees/<int:id>', methods=['DELETE'])
@token_required
def delete_employee(current_user, id):
    # In a real-world scenario, you might restrict deletion to admins
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return '', 204