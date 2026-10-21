from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='participant')
    accessibility_needs = db.Column(db.Text, default='')
    avatar = db.Column(db.String(255), default='')
    is_deaf = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    events = db.relationship('Event', backref='organizer', lazy=True)
    registrations = db.relationship('Registration', backref='user', lazy=True)

    def set_password(self, password):
        """Установить хеш пароля (werkzeug, безопасно)."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверить пароль (поддерживает новый и старый формат)."""
        stored = self.password_hash or ''
        if stored.startswith(('pbkdf2:', 'scrypt:')):
            return check_password_hash(stored, password)
        from utils.auth_helpers import hash_password as legacy_hash
        return legacy_hash(password) == stored


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    is_inclusive = db.Column(db.Boolean, default=False)
    sign_language = db.Column(db.Boolean, default=False)
    visual_alerts = db.Column(db.Boolean, default=False)
    wheelchair_accessible = db.Column(db.Boolean, default=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    registrations = db.relationship('Registration', backref='event', lazy=True)


class Registration(db.Model):
    __tablename__ = 'registrations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    accessibility_request = db.Column(db.Text, default='')

    __table_args__ = (db.UniqueConstraint('user_id', 'event_id'),)
