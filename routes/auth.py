from flask import Blueprint, request, jsonify
from models import db, User
from utils.auth_helpers import hash_password, verify_password, generate_token, token_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not username or not email or not password:
        return jsonify({'error': 'Заполните все поля'}), 400

    # BUG-02 fix: проверка формата email
    if '@' not in email or '.' not in email.split('@')[-1]:
        return jsonify({'error': 'Некорректный email'}), 400

    # BUG-01 fix: явная проверка дубликата → 409
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email уже зарегистрирован'}), 409

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        role=data.get('role', 'participant'),
        accessibility_needs=data.get('accessibility_needs', '')
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Пользователь создан', 'user_id': user.id}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not email or not password:
        return jsonify({'error': 'Введите email и пароль'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password_hash):
        return jsonify({'error': 'Неверный email или пароль'}), 401

    token = generate_token(user.id, user.role)
    return jsonify({'token': token, 'role': user.role, 'user_id': user.id}), 200


@auth_bp.route('/profile', methods=['GET'])
@token_required
def profile(current_user_id, current_user_role):
    user = User.query.get(current_user_id)
    return jsonify({
        'id': user.id, 'username': user.username,
        'email': user.email, 'role': user.role,
        'accessibility_needs': user.accessibility_needs
    }), 200
