
# web/app.py (continued)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import logging

app = Flask(__name__)
app.config.from_object('config.config.Config')

socketio = SocketIO(app)
db = SQLAlchemy(app)

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/start_session', methods=['POST'])
def start_session():
    session_name = request.form.get('session_name')
    if session_name:
        try:
            # Deactivate any active sessions
            active_sessions = Session.query.filter_by(active=True).all()
            for s in active_sessions:
                s.active = False
            # Create new session
            new_session = Session(name=session_name, active=True)
            db.session.add(new_session)
            db.session.commit()
            flash('Session started successfully!', 'success')
            logger.info(f"Session '{session_name}' started.")
        except Exception as e:
            logger.error(f"Error starting session: {e}")
            flash('Failed to start session.', 'error')
    else:
        flash('Session name is required.', 'error')
    return redirect(url_for('dashboard'))

@app.route('/stop_session', methods=['POST'])
def stop_session():
    active_session = Session.query.filter_by(active=True).first()
    if active_session:
        try:
            active_session.active = False
            active_session.duration = (datetime.utcnow() - active_session.date).total_seconds()
            db.session.commit()
            flash('Session stopped successfully!', 'success')
            logger.info(f"Session '{active_session.name}' stopped.")
        except Exception as e:
            logger.error(f"Error stopping session: {e}")
            flash('Failed to stop session.', 'error')
    else:
        flash('No active session found.', 'error')
    return redirect(url_for('dashboard'))

# Models
class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Float, nullable=True)
    active = db.Column(db.Boolean, default=False)
    laps = db.relationship('Lap', backref='session', lazy=True)
    telemetry = db.relationship('Telemetry', backref='session', lazy=True)

class Lap(db.Model):
    __tablename__ = 'laps'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    lap_number = db.Column(db.Integer, nullable=False)
    lap_time = db.Column(db.Float, nullable=False)  # In seconds
    sector_times = db.relationship('SectorTime', backref='lap', lazy=True)
    g_forces = db.relationship('GForce', backref='lap', lazy=True)
    corner_scores = db.relationship('CornerScore', backref='lap', lazy=True)

class SectorTime(db.Model):
    __tablename__ = 'sector_times'
    id = db.Column(db.Integer, primary_key=True)
    lap_id = db.Column(db.Integer, db.ForeignKey('laps.id'), nullable=False)
    sector_number = db.Column(db.Integer, nullable=False)
    sector_time = db.Column(db.Float, nullable=False)  # In seconds

class GForce(db.Model):
    __tablename__ = 'g_forces'
    id = db.Column(db.Integer, primary_key=True)
    lap_id = db.Column(db.Integer, db.ForeignKey('laps.id'), nullable=False)
    lateral = db.Column(db.Float, nullable=False)
    longitudinal = db.Column(db.Float, nullable=False)
    vertical = db.Column(db.Float, nullable=False)

class CornerScore(db.Model):
    __tablename__ = 'corner_scores'
    id = db.Column(db.Integer, primary_key=True)
    lap_id = db.Column(db.Integer, db.ForeignKey('laps.id'), nullable=False)
    corner_number = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float, nullable=False)  # e.g., a score out of 10

class Telemetry(db.Model):
    __tablename__ = 'telemetry'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    speed = db.Column(db.Float)
    acceleration = db.Column(db.Float)
    deceleration = db.Column(db.Float)
    throttle_position = db.Column(db.Float)
    brake_pressure = db.Column(db.Float)
    brake_bias = db.Column(db.Float)
    current_gear = db.Column(db.Integer)
    shift_time = db.Column(db.Float)
    steering_angle = db.Column(db.Float)
    steering_smoothness = db.Column(db.Float)
    engine_rpm = db.Column(db.Integer)
    gear_ratios = db.Column(db.String(50))  # JSON string if multiple ratios
    engine_temperature = db.Column(db.Float)
    tire_temperatures = db.Column(db.String(100))  # JSON string
    tire_wear = db.Column(db.Float)
    tire_pressure = db.Column(db.Float)
    fuel_consumption_rate = db.Column(db.Float)
    remaining_fuel = db.Column(db.Float)
    lap_time = db.Column(db.Float)
    sector_number = db.Column(db.Integer)
    lateral_g = db.Column(db.Float)
    longitudinal_g = db.Column(db.Float)
    vertical_g = db.Column(db.Float)
    ride_height = db.Column(db.Float)
    wing_angles = db.Column(db.String(50))  # JSON string
    damper_spring_rates = db.Column(db.String(50))  # JSON string
    gps_position = db.Column(db.String(50))  # e.g., "lat,lon"
    racing_line_deviation = db.Column(db.Float)
    track_temperature = db.Column(db.Float)
    weather_conditions = db.Column(db.String(50))
    session_duration = db.Column(db.Float)
    number_of_laps = db.Column(db.Integer)
    time_of_day = db.Column(db.String(50))
    # Add more fields as necessary