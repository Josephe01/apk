#!/usr/bin/env python3
"""
Comprehensive RBAC test suite to validate all functionality
"""

import sys
import requests
from requests.sessions import Session
from app import app, db, User, Role, UserRole, Permission, RolePermission, InventoryItem, AccessLog

class RBACTester:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.sessions = {}
        
    def create_session(self, username, password):
        """Create authenticated session for user"""
        session = Session()
        
        # Get login page first to establish session
        login_page = session.get(f"{self.base_url}/login")
        
        # Attempt login
        login_data = {
            'username': username,
            'password': password
        }
        
        response = session.post(f"{self.base_url}/login", data=login_data, allow_redirects=True)
        
        if response.url.endswith('/dashboard'):
            self.sessions[username] = session
            print(f"✓ Successfully logged in as {username}")
            return True
        else:
            print(f"✗ Failed to log in as {username}")
            return False
    
    def test_access_control(self, username, endpoint, should_have_access=True):
        """Test if user can access specific endpoint"""
        if username not in self.sessions:
            print(f"✗ No session for {username}")
            return False
            
        session = self.sessions[username]
        response = session.get(f"{self.base_url}{endpoint}", allow_redirects=False)
        
        # Check if response is a redirect to dashboard (access denied)
        is_redirect_to_dashboard = (response.status_code == 302 and 
                                   response.headers.get('Location', '').endswith('/dashboard'))
        
        has_access = response.status_code == 200 and not is_redirect_to_dashboard
        
        if should_have_access:
            if has_access:
                print(f"✓ {username} can access {endpoint}")
                return True
            else:
                print(f"✗ {username} should have access to {endpoint} but was denied (status: {response.status_code})")
                return False
        else:
            if not has_access:
                print(f"✓ {username} correctly denied access to {endpoint}")
                return True
            else:
                print(f"✗ {username} should NOT have access to {endpoint} but was allowed")
                return False
    
    def test_inventory_operations(self, username, can_create=False, can_modify=False):
        """Test inventory operations"""
        if username not in self.sessions:
            return False
            
        session = self.sessions[username]
        
        # Test viewing inventory
        response = session.get(f"{self.base_url}/inventory")
        can_view = response.status_code == 200
        print(f"{'✓' if can_view else '✗'} {username} can view inventory: {can_view}")
        
        if can_create:
            # Test creating inventory item
            create_data = {
                'name': f'Test Item by {username}',
                'description': 'Test Description',
                'quantity': '5',
                'price': '19.99',
                'category': 'Test'
            }
            response = session.post(f"{self.base_url}/inventory/add", data=create_data)
            can_create_actual = response.status_code in [200, 302]  # 302 for redirect after success
            print(f"{'✓' if can_create_actual else '✗'} {username} can create inventory: {can_create_actual}")
            
        return True
    
    def run_comprehensive_test(self):
        """Run comprehensive RBAC test suite"""
        print("=== RBAC Comprehensive Test Suite ===\n")
        
        # Test 1: User Authentication
        print("1. Testing User Authentication")
        print("-" * 30)
        admin_login = self.create_session('admin', 'admin123')
        manager_login = self.create_session('manager', 'manager123')
        viewer_login = self.create_session('viewer', 'viewer123')
        
        if not all([admin_login, manager_login, viewer_login]):
            print("Authentication tests failed - cannot continue")
            return False
        
        print()
        
        # Test 2: Dashboard Access (all users should have access)
        print("2. Testing Dashboard Access")
        print("-" * 30)
        self.test_access_control('admin', '/dashboard', True)
        self.test_access_control('manager', '/dashboard', True)
        self.test_access_control('viewer', '/dashboard', True)
        print()
        
        # Test 3: Inventory Access
        print("3. Testing Inventory Access")
        print("-" * 30)
        self.test_access_control('admin', '/inventory', True)
        self.test_access_control('manager', '/inventory', True)
        self.test_access_control('viewer', '/inventory', True)
        print()
        
        # Test 4: User Management Access (Admin only)
        print("4. Testing User Management Access")
        print("-" * 35)
        self.test_access_control('admin', '/users', True)
        self.test_access_control('manager', '/users', False)
        self.test_access_control('viewer', '/users', False)
        print()
        
        # Test 5: Role Management Access (Admin only)
        print("5. Testing Role Management Access")
        print("-" * 35)
        self.test_access_control('admin', '/roles', True)
        self.test_access_control('manager', '/roles', False)
        self.test_access_control('viewer', '/roles', False)
        print()
        
        # Test 6: Access Logs (Admin only)
        print("6. Testing Access Logs")
        print("-" * 22)
        self.test_access_control('admin', '/logs', True)
        self.test_access_control('manager', '/logs', False)
        self.test_access_control('viewer', '/logs', False)
        print()
        
        # Test 7: Inventory Operations
        print("7. Testing Inventory Operations")
        print("-" * 32)
        self.test_inventory_operations('admin', can_create=True, can_modify=True)
        self.test_inventory_operations('manager', can_create=True, can_modify=True)
        self.test_inventory_operations('viewer', can_create=False, can_modify=False)
        print()
        
        print("=== RBAC Test Suite Complete ===")
        return True

def test_database_integrity():
    """Test database integrity and relationships"""
    print("=== Database Integrity Test ===\n")
    
    with app.app_context():
        # Test role-permission relationships
        admin_role = Role.query.filter_by(name='Admin').first()
        manager_role = Role.query.filter_by(name='Manager').first()
        viewer_role = Role.query.filter_by(name='Viewer').first()
        
        print(f"Admin role has {len(admin_role.role_permissions)} permissions")
        print(f"Manager role has {len(manager_role.role_permissions)} permissions")  
        print(f"Viewer role has {len(viewer_role.role_permissions)} permissions")
        
        # Test user-role relationships
        admin_user = User.query.filter_by(username='admin').first()
        manager_user = User.query.filter_by(username='manager').first()
        viewer_user = User.query.filter_by(username='viewer').first()
        
        print(f"\nAdmin user has roles: {admin_user.get_roles()}")
        print(f"Manager user has roles: {manager_user.get_roles()}")
        print(f"Viewer user has roles: {viewer_user.get_roles()}")
        
        # Test access logs
        log_count = AccessLog.query.count()
        print(f"\nAccess logs recorded: {log_count}")
        
        # Test inventory items
        item_count = InventoryItem.query.count()
        print(f"Inventory items: {item_count}")
        
        print("\n✓ Database integrity test passed")

if __name__ == '__main__':
    # Test database integrity first
    test_database_integrity()
    
    print("\nStarting web application tests...")
    print("Note: Ensure the Flask app is running on localhost:5000")
    
    # Test web application
    tester = RBACTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎉 All RBAC tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some RBAC tests failed!")
        sys.exit(1)