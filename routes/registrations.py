from flask import Blueprint, request, jsonify
from models import db, Registration, Event, User
from utils.auth_helpers import token_required

reg_bp = Blueprint('registrations', __name__)


@reg_bp.route('/registrations', methods=['POST'])
@token_required
def create_registration(current_user_id, current_user_role):
    data = request.get_json()
    event_id = data.get('event_id')

    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Мероприятие не найдено'}), 404

    existing = Registration.query.filter_by(user_id=current_user_id, event_id=event_id).first()
    if existing:
        return jsonify({'error': 'Вы уже зарегистрированы'}), 409

    reg = Registration(
        user_id=current_user_id,
        event_id=event_id,
        accessibility_request=data.get('accessibility_request', '')
    )
    db.session.add(reg)
    db.session.commit()
    return jsonify({'message': 'Регистрация создана', 'id': reg.id}), 201


@reg_bp.route('/registrations', methods=['GET'])
@token_required
def my_registrations(current_user_id, current_user_role):
    regs = Registration.query.filter_by(user_id=current_user_id).all()
    result = []
    for r in regs:
        result.append({
            'id': r.id,
            'event_id': r.event_id,
            'event_title': r.event.title if r.event else None,
            'registered_at': r.registered_at.isoformat() if r.registered_at else None,
            'accessibility_request': r.accessibility_request
        })
    return jsonify(result), 200
