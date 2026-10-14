from flask import Blueprint, request, jsonify
from models import db, Event
from utils.auth_helpers import token_required, role_required
from utils.accessibility import format_event_response

events_bp = Blueprint('events', __name__)


@events_bp.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([format_event_response(e) for e in events]), 200


@events_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify(format_event_response(event)), 200


@events_bp.route('/events', methods=['POST'])
@role_required(['organizer', 'admin'])
def create_event(current_user_id, current_user_role):
    data = request.get_json()
    event = Event(
        title=data['title'],
        description=data['description'],
        event_date=data['event_date'],
        location=data['location'],
        is_inclusive=data.get('is_inclusive', False),
        sign_language=data.get('sign_language', False),
        visual_alerts=data.get('visual_alerts', False),
        organizer_id=current_user_id
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Мероприятие создано', 'id': event.id}), 201


@events_bp.route('/events/<int:event_id>', methods=['PUT'])
@role_required(['organizer', 'admin'])
def update_event(current_user_id, current_user_role, event_id):
    event = Event.query.get_or_404(event_id)
    data = request.get_json()
    for field in ['title', 'description', 'event_date', 'location',
                  'is_inclusive', 'sign_language', 'visual_alerts']:
        if field in data:
            setattr(event, field, data[field])
    db.session.commit()
    return jsonify({'message': 'Мероприятие обновлено'}), 200


@events_bp.route('/events/<int:event_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_event(current_user_id, current_user_role, event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Мероприятие удалено'}),