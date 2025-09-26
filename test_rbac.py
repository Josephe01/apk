#!/usr/bin/env python3
"""
Test script to verify RBAC functionality
"""

from app import app, db, User, Role, UserRole, Permission, RolePermission, InventoryItem, AccessLog
from werkzeug.security import generate_password_hash

def test_rbac_setup():
    """Test that RBAC is properly set up"""
    
    with app.app_context():
        print("=== RBAC System Test ===")
        
        # Check roles
        roles = Role.query.all()
        print(f"\nRoles created: {len(roles)}")
        for role in roles:
            print(f"  - {role.name}: {role.description}")
            permissions = [rp.permission.name for rp in role.role_permissions]
            print(f"    Permissions: {', '.join(permissions)}")
        
        # Check admin user
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print(f"\nAdmin user created: {admin.username} ({admin.email})")
            admin_roles = admin.get_roles()
            print(f"Admin roles: {admin_roles}")
        
        # Create test users with different roles
        print("\n=== Creating Test Users ===")
        
        # Create Manager user
        manager = User.query.filter_by(username='manager').first()
        if not manager:
            manager = User(username='manager', email='manager@example.com')
            manager.set_password('manager123')
            db.session.add(manager)
            db.session.commit()
            
            # Assign Manager role
            manager_role = Role.query.filter_by(name='Manager').first()
            manager_user_role = UserRole(user_id=manager.id, role_id=manager_role.id, assigned_by=admin.id)
            db.session.add(manager_user_role)
            
            print(f"Created manager user: {manager.username}")
        
        # Create Viewer user
        viewer = User.query.filter_by(username='viewer').first()
        if not viewer:
            viewer = User(username='viewer', email='viewer@example.com')
            viewer.set_password('viewer123')
            db.session.add(viewer)
            db.session.commit()
            
            # Assign Viewer role
            viewer_role = Role.query.filter_by(name='Viewer').first()
            viewer_user_role = UserRole(user_id=viewer.id, role_id=viewer_role.id, assigned_by=admin.id)
            db.session.add(viewer_user_role)
            
            print(f"Created viewer user: {viewer.username}")
        
        db.session.commit()
        
        # Create sample inventory items
        print("\n=== Creating Sample Inventory ===")
        if InventoryItem.query.count() == 0:
            sample_items = [
                InventoryItem(name='Laptop', description='Dell Laptop', quantity=10, price=999.99, category='Electronics', created_by=admin.id),
                InventoryItem(name='Mouse', description='Wireless Mouse', quantity=25, price=29.99, category='Electronics', created_by=admin.id),
                InventoryItem(name='Desk Chair', description='Ergonomic Office Chair', quantity=5, price=199.99, category='Furniture', created_by=admin.id),
                InventoryItem(name='Notebook', description='Spiral Notebook', quantity=100, price=2.99, category='Office Supplies', created_by=admin.id),
            ]
            
            for item in sample_items:
                db.session.add(item)
                print(f"  - {item.name}: {item.quantity} units at ${item.price}")
            
            db.session.commit()
        
        # Test permission checking
        print("\n=== Testing Permission System ===")
        
        manager = User.query.filter_by(username='manager').first()
        viewer = User.query.filter_by(username='viewer').first()
        
        # Test manager permissions
        print(f"\nManager permissions:")
        test_permissions = [('inventory', 'read'), ('inventory', 'create'), ('inventory', 'update'), ('users', 'delete')]
        for resource, action in test_permissions:
            has_perm = has_permission_check(manager, resource, action)
            print(f"  - {resource}:{action} = {has_perm}")
        
        # Test viewer permissions
        print(f"\nViewer permissions:")
        for resource, action in test_permissions:
            has_perm = has_permission_check(viewer, resource, action)
            print(f"  - {resource}:{action} = {has_perm}")
        
        print("\n=== Test Complete ===")
        print("You can now test the web interface with these credentials:")
        print("- Admin: admin / admin123 (full access)")
        print("- Manager: manager / manager123 (inventory management)")
        print("- Viewer: viewer / viewer123 (read-only access)")


def has_permission_check(user, resource, action):
    """Check if user has specific permission (helper function)"""
    for user_role in user.user_roles:
        for role_permission in user_role.role.role_permissions:
            permission = role_permission.permission
            if permission.resource == resource and permission.action == action:
                return True
    return False


if __name__ == '__main__':
    test_rbac_setup()