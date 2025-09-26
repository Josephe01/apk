from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory_rbac.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with roles
    user_roles = db.relationship('UserRole', back_populates='user', cascade='all, delete-orphan', foreign_keys='UserRole.user_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role_name):
        return any(ur.role.name == role_name for ur in self.user_roles)
    
    def get_roles(self):
        return [ur.role.name for ur in self.user_roles]

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with users
    user_roles = db.relationship('UserRole', back_populates='role', cascade='all, delete-orphan')
    # Relationship with permissions
    role_permissions = db.relationship('RolePermission', back_populates='role', cascade='all, delete-orphan')

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    resource = db.Column(db.String(50), nullable=False)  # e.g., 'inventory', 'users', 'roles'
    action = db.Column(db.String(50), nullable=False)    # e.g., 'create', 'read', 'update', 'delete'
    
    # Relationship with roles
    role_permissions = db.relationship('RolePermission', back_populates='permission', cascade='all, delete-orphan')

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    user = db.relationship('User', back_populates='user_roles', foreign_keys=[user_id])
    role = db.relationship('Role', back_populates='user_roles')
    assigner = db.relationship('User', foreign_keys=[assigned_by])

class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), nullable=False)
    
    # Relationships
    role = db.relationship('Role', back_populates='role_permissions')
    permission = db.relationship('Permission', back_populates='role_permissions')

class AccessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    resource = db.Column(db.String(50), nullable=False)
    resource_id = db.Column(db.String(50))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    success = db.Column(db.Boolean, default=True)
    details = db.Column(db.Text)
    
    # Relationship
    user = db.relationship('User')

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Float)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationship
    creator = db.relationship('User')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Access Control Decorators
def require_role(role_name):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not current_user.has_role(role_name):
                log_access(current_user.id, f"Access denied to {f.__name__}", "authorization", success=False)
                flash(f'Access denied. Required role: {role_name}', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_permission(resource, action):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not has_permission(current_user, resource, action):
                log_access(current_user.id, f"Permission denied: {action} on {resource}", resource, success=False)
                flash(f'Permission denied. Required: {action} on {resource}', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_role_any(*roles):
    """Decorator that requires user to have any of the specified roles"""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            user_roles = current_user.get_roles()
            if not any(role in user_roles for role in roles):
                log_access(current_user.id, f"Access denied to {f.__name__}", "authorization", success=False)
                flash(f'Access denied. Required roles: {", ".join(roles)}', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def has_permission(user, resource, action):
    """Check if user has specific permission"""
    for user_role in user.user_roles:
        for role_permission in user_role.role.role_permissions:
            permission = role_permission.permission
            if permission.resource == resource and permission.action == action:
                return True
    return False

def log_access(user_id, action, resource, resource_id=None, success=True, details=None):
    """Log user access for auditing"""
    log_entry = AccessLog(
        user_id=user_id,
        action=action,
        resource=resource,
        resource_id=resource_id,
        ip_address=request.remote_addr if request else None,
        user_agent=request.headers.get('User-Agent') if request else None,
        success=success,
        details=details
    )
    db.session.add(log_entry)
    db.session.commit()

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            log_access(user.id, 'User login', 'authentication')
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            if user:
                log_access(user.id, 'Failed login attempt', 'authentication', success=False)
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    log_access(current_user.id, 'User logout', 'authentication')
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    log_access(current_user.id, 'Accessed dashboard', 'dashboard')
    
    # Get user's roles and permissions
    user_roles = current_user.get_roles()
    
    # Get some basic stats based on permissions
    stats = {}
    if has_permission(current_user, 'inventory', 'read'):
        stats['inventory_count'] = InventoryItem.query.count()
    
    if has_permission(current_user, 'users', 'read'):
        stats['user_count'] = User.query.count()
    
    if has_permission(current_user, 'logs', 'read'):
        stats['recent_logs'] = AccessLog.query.order_by(AccessLog.timestamp.desc()).limit(5).all()
    
    return render_template('dashboard.html', user_roles=user_roles, stats=stats)

@app.route('/inventory')
@login_required
@require_role_any('Admin', 'Manager', 'Viewer')
def inventory():
    log_access(current_user.id, 'Viewed inventory', 'inventory')
    items = InventoryItem.query.all()
    can_modify = has_permission(current_user, 'inventory', 'update') or has_permission(current_user, 'inventory', 'create')
    can_delete = has_permission(current_user, 'inventory', 'delete')
    return render_template('inventory.html', items=items, can_modify=can_modify, can_delete=can_delete)

@app.route('/inventory/add', methods=['GET', 'POST'])
@login_required
@require_role_any('Admin', 'Manager')
def add_inventory():
    if request.method == 'POST':
        item = InventoryItem(
            name=request.form['name'],
            description=request.form['description'],
            quantity=int(request.form['quantity']),
            price=float(request.form['price']) if request.form['price'] else None,
            category=request.form['category'],
            created_by=current_user.id
        )
        db.session.add(item)
        db.session.commit()
        
        log_access(current_user.id, 'Created inventory item', 'inventory', str(item.id), details=f"Item: {item.name}")
        flash('Inventory item added successfully!', 'success')
        return redirect(url_for('inventory'))
    
    return render_template('add_inventory.html')

@app.route('/inventory/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
@require_role_any('Admin', 'Manager')
def edit_inventory(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.quantity = int(request.form['quantity'])
        item.price = float(request.form['price']) if request.form['price'] else None
        item.category = request.form['category']
        item.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        log_access(current_user.id, 'Updated inventory item', 'inventory', str(item.id), details=f"Item: {item.name}")
        flash('Inventory item updated successfully!', 'success')
        return redirect(url_for('inventory'))
    
    return render_template('edit_inventory.html', item=item)

@app.route('/inventory/delete/<int:item_id>', methods=['POST'])
@login_required
@require_role_any('Admin', 'Manager')
def delete_inventory(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    item_name = item.name
    
    db.session.delete(item)
    db.session.commit()
    
    log_access(current_user.id, 'Deleted inventory item', 'inventory', str(item_id), details=f"Item: {item_name}")
    flash('Inventory item deleted successfully!', 'success')
    return redirect(url_for('inventory'))

@app.route('/users')
@login_required  
@require_role('Admin')
def users():
    log_access(current_user.id, 'Viewed users list', 'users')
    users_list = User.query.all()
    can_modify = has_permission(current_user, 'users', 'update')
    can_assign_roles = has_permission(current_user, 'roles', 'assign')
    return render_template('users.html', users=users_list, can_modify=can_modify, can_assign_roles=can_assign_roles)

@app.route('/users/<int:user_id>/roles', methods=['GET', 'POST'])
@login_required
@require_role('Admin')
def manage_user_roles(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # Remove existing roles
        UserRole.query.filter_by(user_id=user_id).delete()
        
        # Add selected roles
        selected_roles = request.form.getlist('roles')
        for role_id in selected_roles:
            user_role = UserRole(user_id=user_id, role_id=int(role_id), assigned_by=current_user.id)
            db.session.add(user_role)
        
        db.session.commit()
        
        log_access(current_user.id, 'Modified user roles', 'roles', str(user_id), 
                  details=f"User: {user.username}, Roles: {selected_roles}")
        flash(f'Roles updated for user {user.username}!', 'success')
        return redirect(url_for('users'))
    
    all_roles = Role.query.all()
    user_role_ids = [ur.role_id for ur in user.user_roles]
    
    return render_template('manage_roles.html', user=user, all_roles=all_roles, user_role_ids=user_role_ids)

@app.route('/roles')
@login_required
@require_role('Admin')
def roles():
    log_access(current_user.id, 'Viewed roles list', 'roles')
    roles_list = Role.query.all()
    can_modify = has_permission(current_user, 'roles', 'update')
    return render_template('roles.html', roles=roles_list, can_modify=can_modify)

@app.route('/logs')
@login_required
@require_role('Admin')
def access_logs():
    log_access(current_user.id, 'Viewed access logs', 'logs')
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    logs = AccessLog.query.order_by(AccessLog.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('logs.html', logs=logs)

# API Routes for AJAX requests
@app.route('/api/user-permissions/<int:user_id>')
@login_required
@require_role('Admin')
def get_user_permissions(user_id):
    user = User.query.get_or_404(user_id)
    permissions = []
    
    for user_role in user.user_roles:
        for role_permission in user_role.role.role_permissions:
            permission = role_permission.permission
            permissions.append({
                'name': permission.name,
                'description': permission.description,
                'resource': permission.resource,
                'action': permission.action,
                'role': user_role.role.name
            })
    
    return jsonify(permissions)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create default roles and permissions if they don't exist
        if not Role.query.first():
            # Create roles
            admin_role = Role(name='Admin', description='Full system access')
            manager_role = Role(name='Manager', description='Can manage inventory and view reports')
            viewer_role = Role(name='Viewer', description='Read-only access to inventory')
            
            db.session.add_all([admin_role, manager_role, viewer_role])
            db.session.commit()
            
            # Create permissions
            permissions = [
                # User management
                Permission(name='create_user', description='Create new users', resource='users', action='create'),
                Permission(name='read_user', description='View user information', resource='users', action='read'),
                Permission(name='update_user', description='Update user information', resource='users', action='update'),
                Permission(name='delete_user', description='Delete users', resource='users', action='delete'),
                
                # Role management
                Permission(name='create_role', description='Create new roles', resource='roles', action='create'),
                Permission(name='read_role', description='View role information', resource='roles', action='read'),
                Permission(name='update_role', description='Update role information', resource='roles', action='update'),
                Permission(name='delete_role', description='Delete roles', resource='roles', action='delete'),
                Permission(name='assign_role', description='Assign roles to users', resource='roles', action='assign'),
                
                # Inventory management
                Permission(name='create_inventory', description='Create inventory items', resource='inventory', action='create'),
                Permission(name='read_inventory', description='View inventory items', resource='inventory', action='read'),
                Permission(name='update_inventory', description='Update inventory items', resource='inventory', action='update'),
                Permission(name='delete_inventory', description='Delete inventory items', resource='inventory', action='delete'),
                
                # Access logs
                Permission(name='read_logs', description='View access logs', resource='logs', action='read'),
            ]
            
            db.session.add_all(permissions)
            db.session.commit()
            
            # Assign permissions to roles
            # Admin gets all permissions
            admin_permissions = Permission.query.all()
            for permission in admin_permissions:
                role_permission = RolePermission(role_id=admin_role.id, permission_id=permission.id)
                db.session.add(role_permission)
            
            # Manager gets inventory and some user permissions
            manager_permission_names = ['read_user', 'create_inventory', 'read_inventory', 'update_inventory', 'read_logs']
            manager_permissions = Permission.query.filter(Permission.name.in_(manager_permission_names)).all()
            for permission in manager_permissions:
                role_permission = RolePermission(role_id=manager_role.id, permission_id=permission.id)
                db.session.add(role_permission)
            
            # Viewer gets only read permissions
            viewer_permission_names = ['read_user', 'read_inventory']
            viewer_permissions = Permission.query.filter(Permission.name.in_(viewer_permission_names)).all()
            for permission in viewer_permissions:
                role_permission = RolePermission(role_id=viewer_role.id, permission_id=permission.id)
                db.session.add(role_permission)
            
            db.session.commit()
            
            # Create default admin user
            admin_user = User(username='admin', email='admin@example.com')
            admin_user.set_password('admin123')  # Change this in production!
            db.session.add(admin_user)
            db.session.commit()
            
            # Assign admin role to admin user
            admin_user_role = UserRole(user_id=admin_user.id, role_id=admin_role.id)
            db.session.add(admin_user_role)
            db.session.commit()
            
            print("Database initialized with default roles, permissions, and admin user.")
            print("Admin credentials: username='admin', password='admin123'")
    
    app.run(debug=True)