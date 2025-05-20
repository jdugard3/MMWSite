from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models import db, User
from ..utils import APIException

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    
    if not data:
        raise APIException("No data provided", status_code=400)
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        raise APIException("Email already registered", status_code=400)
    
    # Create new user
    user = User(
        email=data['email'],
        first_name=data.get('first_name'),
        last_name=data.get('last_name')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.serialize()), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    
    if not data:
        raise APIException("No data provided", status_code=400)
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        raise APIException("Invalid email or password", status_code=401)
    
    if not user.is_active:
        raise APIException("Account is inactive", status_code=401)
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        "access_token": access_token,
        "user": user.serialize()
    }), 200

@auth.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        raise APIException("User not found", status_code=404)
    
    return jsonify(user.serialize()), 200

@auth.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        raise APIException("User not found", status_code=404)
    
    data = request.json
    
    if not data:
        raise APIException("No data provided", status_code=400)
    
    # Update user fields
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'password' in data:
        user.set_password(data['password'])
    
    db.session.commit()
    
    return jsonify(user.serialize()), 200 