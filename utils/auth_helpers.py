import jwt
import datetime
import hashlib
from functools import wraps
from flask import request, jsonify, current_app


def hash_password(password):
    """Хеширование пароля с солью."""
    salt = 'accessevent_salt_2025'
    return hashlib.sha256((password + salt).encode()).hexdigest()


def verify_password(password, password_hash):
    """Проверка пароля."""
    return hash_password(password) == password_hash


def generate_token(user_id, role):
    """Генерация JWT-токена."""
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token


def token_required(f):
    """Декоратор: проверка JWT."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        if not token:
            return jsonify({'error': 'Токен отсутствует'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
            current_user_role = data['role']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Токен истёк'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Неверный токен'}), 401
        return f(current_user_id, current_user_role, *args, **kwargs)
    return decorated


def role_required(roles):
    """Декоратор: проверка роли."""
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(current_user_id, current_user_role, *args, **kwargs):
            if current_user_role not in roles:
                return jsonify({'error': 'Недостаточно прав'}), 403
            return f(current_user_id, current_user_role, *args, **kwargs)
        return decorated
    return decorator