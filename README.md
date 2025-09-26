# Inventory Management System with Role-Based Access Control (RBAC)

A comprehensive inventory management system implementing secure Role-Based Access Control (RBAC) for enhanced security and structured access management.

## Features

### 🔐 Role-Based Access Control (RBAC)
- **Admin Role**: Full system access including user management, role assignment, and access to all features and logs
- **Manager Role**: Can manage inventory items, view reports, and access user information but cannot modify user roles
- **Viewer Role**: Read-only access to inventory and basic user information

### 📊 Inventory Management
- Create, read, update, and delete inventory items
- Role-based permissions for inventory operations
- Comprehensive item tracking with timestamps and user attribution

### 👥 User Management
- User authentication and session management
- Admin-only user role assignment
- Secure user creation and management

### 📝 Access Logging & Auditing
- Complete audit trail of all user actions
- Access attempt logging (both successful and failed)
- Timestamp and IP address tracking
- Detailed activity monitoring

### 🛡️ Security Features
- Secure password hashing using Werkzeug
- Session-based authentication with Flask-Login
- Role validation that cannot be bypassed
- CSRF protection ready
- Input validation and sanitization

## Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd apk
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
```

4. **Access the application:**
Open your browser and navigate to `http://localhost:5000`

### Default Credentials

The system initializes with three test users:

| Username | Password | Role | Access Level |
|----------|----------|------|--------------|
| admin | admin123 | Admin | Full system access |
| manager | manager123 | Manager | Inventory management |
| viewer | viewer123 | Viewer | Read-only access |

**⚠️ Important**: Change these default passwords in production!

## Architecture

### Database Models

- **User**: User accounts with authentication
- **Role**: System roles (Admin, Manager, Viewer)
- **Permission**: Granular permissions for specific actions
- **UserRole**: Many-to-many relationship between users and roles
- **RolePermission**: Many-to-many relationship between roles and permissions
- **AccessLog**: Audit trail of all user actions
- **InventoryItem**: Inventory management with full CRUD operations

### Access Control Matrix

| Feature | Admin | Manager | Viewer |
|---------|-------|---------|--------|
| Dashboard | ✅ | ✅ | ✅ |
| View Inventory | ✅ | ✅ | ✅ |
| Create Inventory | ✅ | ✅ | ❌ |
| Edit Inventory | ✅ | ✅ | ❌ |
| Delete Inventory | ✅ | ✅ | ❌ |
| User Management | ✅ | ❌ | ❌ |
| Role Management | ✅ | ❌ | ❌ |
| Access Logs | ✅ | ❌ | ❌ |

## Testing

### Run Comprehensive Tests

```bash
# Test database integrity and RBAC functionality
python test_rbac.py

# Run comprehensive web application tests
python test_complete_rbac.py
```

### Manual Testing

1. **Login with different users** to verify role-based access
2. **Try accessing restricted pages** to ensure proper access denial
3. **Check access logs** to verify audit trail functionality
4. **Test inventory operations** with different user roles

## API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - User authentication
- `GET /logout` - User logout

### Dashboard & Navigation
- `GET /` - Redirect to dashboard
- `GET /dashboard` - Main dashboard (all roles)

### Inventory Management
- `GET /inventory` - View inventory (all roles)
- `GET /inventory/add` - Add inventory form (Admin, Manager)
- `POST /inventory/add` - Create inventory item (Admin, Manager)
- `GET /inventory/edit/<id>` - Edit inventory form (Admin, Manager)
- `POST /inventory/edit/<id>` - Update inventory item (Admin, Manager)
- `POST /inventory/delete/<id>` - Delete inventory item (Admin, Manager)

### User & Role Management (Admin Only)
- `GET /users` - User management page
- `GET /users/<id>/roles` - Role assignment form
- `POST /users/<id>/roles` - Update user roles
- `GET /roles` - Role management page

### Access Logs (Admin Only)
- `GET /logs` - View access logs

### API Endpoints
- `GET /api/user-permissions/<id>` - Get user permissions (Admin only)

## Security Implementation

### Access Control Decorators

```python
@require_role('Admin')  # Requires specific role
@require_role_any('Admin', 'Manager')  # Requires any of the specified roles
@require_permission('resource', 'action')  # Requires specific permission
```

### Audit Logging

All user actions are automatically logged with:
- User ID and username
- Action performed
- Resource accessed
- Timestamp
- IP address and user agent
- Success/failure status
- Additional details

### Password Security

- Passwords are hashed using Werkzeug's secure password hashing
- No plaintext passwords stored in database
- Session-based authentication

## Production Deployment

### Security Checklist

1. **Change default credentials**
2. **Update SECRET_KEY** in production
3. **Use PostgreSQL or MySQL** instead of SQLite
4. **Enable HTTPS** for all connections
5. **Set up proper logging** and monitoring
6. **Configure firewalls** and security groups
7. **Regular security audits** and updates

### Environment Variables

Create a `.env` file for production:

```env
SECRET_KEY=your-secure-secret-key
DATABASE_URL=postgresql://user:password@localhost/inventory_db
FLASK_ENV=production
```

### Docker Deployment

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## Development

### Project Structure

```
apk/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── login.html        # Login page
│   ├── dashboard.html    # Dashboard
│   ├── inventory.html    # Inventory listing
│   ├── users.html        # User management
│   └── ...
├── test_rbac.py          # Basic RBAC tests
├── test_complete_rbac.py # Comprehensive test suite
└── README.md            # This file
```

### Adding New Roles

1. **Create role in database:**
```python
new_role = Role(name='NewRole', description='Description')
db.session.add(new_role)
db.session.commit()
```

2. **Assign permissions:**
```python
permissions = Permission.query.filter(Permission.name.in_(['permission1', 'permission2'])).all()
for permission in permissions:
    role_permission = RolePermission(role_id=new_role.id, permission_id=permission.id)
    db.session.add(role_permission)
db.session.commit()
```

3. **Update access control decorators** in route handlers
4. **Update navigation template** to show/hide features based on role

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the test files for usage examples
- Review the access logs for debugging authentication issues