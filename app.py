from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.String(200), nullable=False)

@app.route('/api/v1/calendar/add', methods=['POST'])
def add_event():
    data = request.get_json()

    try:
        event_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    if len(data['title']) > 30 or len(data['text']) > 200:
        return jsonify({'error': 'Title or text exceeds maximum length'}), 400

    existing_event = Event.query.filter_by(date=event_date).first()
    if existing_event:
        return jsonify({'error': 'Event already exists for this date'}), 409

    new_event = Event(date=event_date, title=data['title'], text=data['text'])

    try:
        db.session.add(new_event)
        db.session.commit()
        return jsonify({'message': 'Event added successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'IntegrityError'}), 500

@app.route('/api/v1/calendar/list', methods=['GET'])
def list_events():
    events = Event.query.all()
    event_list = [{'id': event.id, 'date': str(event.date), 'title': event.title, 'text': event.text} for event in events]
    return jsonify({'events': event_list})

@app.route('/api/v1/calendar/read/<int:event_id>', methods=['GET'])
def read_event(event_id):
    event = Event.query.get(event_id)
    if event:
        return jsonify({'id': event.id, 'date': str(event.date), 'title': event.title, 'text': event.text})
    else:
        return jsonify({'error': 'Event not found'}), 404

@app.route('/api/v1/calendar/update/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    data = request.get_json()

    try:
        if 'date' in data:
            event.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'title' in data:
            if len(data['title']) > 30:
                return jsonify({'error': 'Title exceeds maximum length'}), 400
            event.title = data['title']
        if 'text' in data:
            if len(data['text']) > 200:
                return jsonify({'error': 'Text exceeds maximum length'}), 400
            event.text = data['text']

        db.session.commit()
        return jsonify({'message': 'Event updated successfully'}), 200
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'IntegrityError'}), 500

@app.route('/api/v1/calendar/delete/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Event deleted successfully'}), 200
    else:
        return jsonify({'error': 'Event not found'}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    
