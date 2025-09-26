#!/usr/bin/env python3
"""
Advanced Inventory Management System with Live Monitoring
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import uuid
import json
import os
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import csv
import io

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///inventory.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin, manager, user
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    audit_sessions = db.relationship('AuditSession', backref='user', lazy=True)
    audit_logs = db.relationship('AuditLog', backref='user', lazy=True)

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    barcode = db.Column(db.String(100), unique=True)
    expected_quantity = db.Column(db.Integer, default=0)
    actual_quantity = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50))
    location = db.Column(db.String(100))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    audit_logs = db.relationship('AuditLog', backref='item', lazy=True)

class AuditSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    items_scanned = db.Column(db.Integer, default=0)
    discrepancies_found = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    
    # Relationships
    audit_logs = db.relationship('AuditLog', backref='session', lazy=True)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('audit_session.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_item.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # scan, adjust, note
    old_quantity = db.Column(db.Integer)
    new_quantity = db.Column(db.Integer)
    discrepancy = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    """Main dashboard"""
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    # Get active audit sessions
    active_sessions = AuditSession.query.filter_by(status='active').all()
    
    # Get recent inventory updates
    recent_items = InventoryItem.query.order_by(InventoryItem.last_updated.desc()).limit(10).all()
    
    return render_template('dashboard.html', 
                         active_sessions=active_sessions, 
                         recent_items=recent_items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('login'))

@app.route('/inventory')
@login_required
def inventory():
    """Inventory management page"""
    items = InventoryItem.query.all()
    return render_template('inventory.html', items=items)

@app.route('/start_audit', methods=['POST'])
@login_required
def start_audit():
    """Start a new inventory audit session"""
    # Check if user already has an active session
    existing_session = AuditSession.query.filter_by(
        user_id=current_user.id, 
        status='active'
    ).first()
    
    if existing_session:
        return jsonify({
            'success': False, 
            'message': 'You already have an active audit session'
        }), 400
    
    # Create new session
    session = AuditSession(user_id=current_user.id)
    db.session.add(session)
    db.session.commit()
    
    # Notify all users about new session
    socketio.emit('audit_started', {
        'session_id': session.session_id,
        'user': current_user.username,
        'start_time': session.start_time.isoformat(),
        'items_scanned': 0,
        'discrepancies_found': 0
    }, room='all_users')
    
    return jsonify({
        'success': True, 
        'session_id': session.session_id,
        'message': 'Audit session started successfully'
    })

@app.route('/audit/<session_id>')
@login_required
def audit_interface(session_id):
    """Audit interface for scanning items"""
    session = AuditSession.query.filter_by(
        session_id=session_id, 
        status='active'
    ).first_or_404()
    
    # Check if user owns this session
    if session.user_id != current_user.id:
        return redirect(url_for('index'))
    
    items = InventoryItem.query.all()
    return render_template('audit.html', session=session, items=items)

# API Routes
@app.route('/api/active_session')
@login_required
def get_active_session():
    """Get currently active audit session"""
    session = AuditSession.query.filter_by(status='active').first()
    if session:
        return jsonify({
            'session': {
                'session_id': session.session_id,
                'user': session.user.username,
                'start_time': session.start_time.isoformat(),
                'items_scanned': session.items_scanned,
                'discrepancies_found': session.discrepancies_found
            }
        })
    return jsonify({'session': None})

@app.route('/api/session/<session_id>')
@login_required
def get_session_details(session_id):
    """Get session details"""
    session = AuditSession.query.filter_by(session_id=session_id).first_or_404()
    
    return jsonify({
        'session_id': session.session_id,
        'user': session.user.username,
        'start_time': session.start_time.isoformat(),
        'end_time': session.end_time.isoformat() if session.end_time else None,
        'status': session.status,
        'items_scanned': session.items_scanned,
        'discrepancies_found': session.discrepancies_found,
        'notes': session.notes
    })

@app.route('/api/session/<session_id>/end', methods=['POST'])
@login_required
def end_audit_session(session_id):
    """End an audit session"""
    session = AuditSession.query.filter_by(
        session_id=session_id,
        user_id=current_user.id,
        status='active'
    ).first_or_404()
    
    session.end_time = datetime.utcnow()
    session.status = 'completed'
    session.notes = request.json.get('notes', '')
    
    db.session.commit()
    
    # Notify all users
    socketio.emit('audit_completed', {
        'session_id': session.session_id,
        'user': current_user.username,
        'end_time': session.end_time.isoformat(),
        'items_scanned': session.items_scanned,
        'discrepancies_found': session.discrepancies_found
    }, room='all_users')
    
    return jsonify({
        'success': True,
        'message': 'Audit session completed successfully'
    })

@app.route('/api/scan', methods=['POST'])
@login_required
def scan_item():
    """Scan an item during audit"""
    data = request.json
    session_id = data.get('session_id')
    barcode = data.get('barcode')
    actual_quantity = data.get('actual_quantity')
    
    # Get active session
    session = AuditSession.query.filter_by(
        session_id=session_id,
        user_id=current_user.id,
        status='active'
    ).first()
    
    if not session:
        return jsonify({'success': False, 'message': 'Invalid session'}), 400
    
    # Find item by barcode or SKU
    item = InventoryItem.query.filter(
        (InventoryItem.barcode == barcode) | (InventoryItem.sku == barcode)
    ).first()
    
    if not item:
        return jsonify({'success': False, 'message': 'Item not found'}), 404
    
    # Record audit log
    old_quantity = item.actual_quantity
    discrepancy = actual_quantity - item.expected_quantity
    
    audit_log = AuditLog(
        session_id=session.id,
        user_id=current_user.id,
        item_id=item.id,
        action='scan',
        old_quantity=old_quantity,
        new_quantity=actual_quantity,
        discrepancy=discrepancy,
        notes=data.get('notes', '')
    )
    
    # Update item quantity
    item.actual_quantity = actual_quantity
    item.last_updated = datetime.utcnow()
    
    # Update session stats
    session.items_scanned += 1
    if discrepancy != 0:
        session.discrepancies_found += 1
    
    db.session.add(audit_log)
    db.session.commit()
    
    # Emit real-time updates
    socketio.emit('item_scanned', {
        'item_id': item.id,
        'item_name': item.name,
        'actual_quantity': actual_quantity,
        'expected_quantity': item.expected_quantity,
        'discrepancy': discrepancy
    }, room='all_users')
    
    socketio.emit('audit_updated', {
        'session_id': session.session_id,
        'items_scanned': session.items_scanned,
        'discrepancies_found': session.discrepancies_found
    }, room='all_users')
    
    if discrepancy != 0:
        socketio.emit('discrepancy_found', {
            'item_name': item.name,
            'discrepancy': discrepancy,
            'expected': item.expected_quantity,
            'actual': actual_quantity
        }, room='all_users')
    
    return jsonify({
        'success': True,
        'item': {
            'id': item.id,
            'name': item.name,
            'expected_quantity': item.expected_quantity,
            'actual_quantity': actual_quantity,
            'discrepancy': discrepancy
        }
    })

@app.route('/api/item', methods=['POST'])
@login_required
def add_item():
    """Add new inventory item"""
    if current_user.role not in ['admin', 'manager']:
        return jsonify({'success': False, 'message': 'Insufficient permissions'}), 403
    
    data = request.json
    
    # Check if SKU already exists
    existing_item = InventoryItem.query.filter_by(sku=data['sku']).first()
    if existing_item:
        return jsonify({'success': False, 'message': 'SKU already exists'}), 400
    
    item = InventoryItem(
        name=data['name'],
        sku=data['sku'],
        barcode=data.get('barcode'),
        category=data.get('category'),
        location=data.get('location'),
        expected_quantity=data.get('expected_quantity', 0),
        actual_quantity=data.get('actual_quantity', 0)
    )
    
    db.session.add(item)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Item added successfully'})

@app.route('/api/item/<int:item_id>', methods=['GET'])
@login_required
def get_item(item_id):
    """Get item details"""
    item = InventoryItem.query.get_or_404(item_id)
    
    return jsonify({
        'id': item.id,
        'name': item.name,
        'sku': item.sku,
        'barcode': item.barcode,
        'category': item.category,
        'location': item.location,
        'expected_quantity': item.expected_quantity,
        'actual_quantity': item.actual_quantity,
        'last_updated': item.last_updated.isoformat()
    })

@app.route('/api/item/<int:item_id>', methods=['PUT'])
@login_required
def update_item(item_id):
    """Update inventory item"""
    if current_user.role not in ['admin', 'manager']:
        return jsonify({'success': False, 'message': 'Insufficient permissions'}), 403
    
    item = InventoryItem.query.get_or_404(item_id)
    data = request.json
    
    item.name = data['name']
    item.sku = data['sku']
    item.barcode = data.get('barcode')
    item.category = data.get('category')
    item.location = data.get('location')
    item.expected_quantity = data.get('expected_quantity', 0)
    item.actual_quantity = data.get('actual_quantity', 0)
    item.last_updated = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Item updated successfully'})

@app.route('/api/item/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item(item_id):
    """Delete inventory item"""
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Insufficient permissions'}), 403
    
    item = InventoryItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Item deleted successfully'})

@app.route('/api/session/<session_id>/export')
@login_required
def export_session_report(session_id):
    """Export session report as PDF or CSV"""
    session = AuditSession.query.filter_by(session_id=session_id).first_or_404()
    format_type = request.args.get('format', 'pdf')
    
    # Get audit logs for this session
    logs = AuditLog.query.filter_by(session_id=session.id).all()
    
    if format_type == 'pdf':
        return generate_pdf_report(session, logs)
    elif format_type == 'csv':
        return generate_csv_report(session, logs)
    else:
        return jsonify({'error': 'Invalid format'}), 400

def generate_pdf_report(session, logs):
    """Generate PDF report"""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, f"Inventory Audit Report - Session {session.session_id}")
    
    # Session details
    p.setFont("Helvetica", 12)
    y = 720
    p.drawString(50, y, f"User: {session.user.username}")
    y -= 20
    p.drawString(50, y, f"Start Time: {session.start_time}")
    y -= 20
    if session.end_time:
        p.drawString(50, y, f"End Time: {session.end_time}")
        y -= 20
    p.drawString(50, y, f"Items Scanned: {session.items_scanned}")
    y -= 20
    p.drawString(50, y, f"Discrepancies Found: {session.discrepancies_found}")
    y -= 40
    
    # Audit logs
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Audit Log:")
    y -= 30
    
    p.setFont("Helvetica", 10)
    for log in logs:
        if y < 50:  # New page
            p.showPage()
            y = 750
        
        p.drawString(50, y, f"{log.timestamp} - {log.item.name} ({log.item.sku})")
        y -= 15
        p.drawString(70, y, f"Action: {log.action}, Old: {log.old_quantity}, New: {log.new_quantity}, Discrepancy: {log.discrepancy}")
        y -= 20
    
    p.save()
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name=f'audit_report_{session.session_id}.pdf', mimetype='application/pdf')

def generate_csv_report(session, logs):
    """Generate CSV report"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Session Info'])
    writer.writerow(['Session ID', session.session_id])
    writer.writerow(['User', session.user.username])
    writer.writerow(['Start Time', session.start_time])
    writer.writerow(['End Time', session.end_time or 'Active'])
    writer.writerow(['Items Scanned', session.items_scanned])
    writer.writerow(['Discrepancies Found', session.discrepancies_found])
    writer.writerow([])
    
    # Audit logs
    writer.writerow(['Audit Logs'])
    writer.writerow(['Timestamp', 'Item Name', 'SKU', 'Action', 'Old Quantity', 'New Quantity', 'Discrepancy', 'Notes'])
    
    for log in logs:
        writer.writerow([
            log.timestamp,
            log.item.name,
            log.item.sku,
            log.action,
            log.old_quantity,
            log.new_quantity,
            log.discrepancy,
            log.notes or ''
        ])
    
    buffer = io.BytesIO()
    buffer.write(output.getvalue().encode('utf-8'))
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name=f'audit_report_{session.session_id}.csv', mimetype='text/csv')

# WebSocket Events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    if current_user.is_authenticated:
        join_room('all_users')
        emit('connected', {'message': 'Connected to inventory system'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    if current_user.is_authenticated:
        leave_room('all_users')

@socketio.on('join_room')
def handle_join_room(room):
    """Handle joining a room"""
    if current_user.is_authenticated:
        join_room(room)
        emit('joined_room', {'room': room})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create default admin user if none exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@inventory.com',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            
            # Add sample inventory items
            sample_items = [
                InventoryItem(name='Laptop Dell XPS 13', sku='LAPTOP-001', barcode='123456789', expected_quantity=10, actual_quantity=10, category='Electronics', location='Shelf A1'),
                InventoryItem(name='Wireless Mouse', sku='MOUSE-001', barcode='123456790', expected_quantity=25, actual_quantity=23, category='Accessories', location='Shelf B2'),
                InventoryItem(name='USB Cable Type-C', sku='CABLE-001', barcode='123456791', expected_quantity=50, actual_quantity=48, category='Cables', location='Drawer C1'),
                InventoryItem(name='Monitor 24 inch', sku='MONITOR-001', barcode='123456792', expected_quantity=8, actual_quantity=8, category='Electronics', location='Shelf A2'),
                InventoryItem(name='Keyboard Mechanical', sku='KEYBOARD-001', barcode='123456793', expected_quantity=15, actual_quantity=14, category='Accessories', location='Shelf B1'),
            ]
            
            for item in sample_items:
                db.session.add(item)
            
            db.session.commit()
            print("Default admin user created (username: admin, password: admin123)")
            print("Sample inventory items added")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)