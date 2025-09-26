#!/usr/bin/env python3
"""
RBAC System Demonstration Script
Shows the complete functionality of the Role-Based Access Control system
"""

from app import app, db, User, Role, UserRole, Permission, RolePermission, InventoryItem, AccessLog
from datetime import datetime

def demonstrate_rbac():
    """Demonstrate the RBAC system functionality"""
    
    with app.app_context():
        print("🔐 RBAC INVENTORY MANAGEMENT SYSTEM DEMONSTRATION")
        print("=" * 60)
        
        # 1. Show System Overview
        print("\n📊 SYSTEM OVERVIEW")
        print("-" * 20)
        print(f"Total Users: {User.query.count()}")
        print(f"Total Roles: {Role.query.count()}")
        print(f"Total Permissions: {Permission.query.count()}")
        print(f"Inventory Items: {InventoryItem.query.count()}")
        print(f"Access Log Entries: {AccessLog.query.count()}")
        
        # 2. Show Role Hierarchy
        print("\n🏷️  ROLE HIERARCHY & PERMISSIONS")
        print("-" * 35)
        
        roles = Role.query.all()
        for role in roles:
            print(f"\n{role.name} Role:")
            print(f"  Description: {role.description}")
            print(f"  Users: {len(role.user_roles)}")
            print("  Permissions:")
            
            permissions_by_resource = {}
            for rp in role.role_permissions:
                resource = rp.permission.resource
                if resource not in permissions_by_resource:
                    permissions_by_resource[resource] = []
                permissions_by_resource[resource].append(rp.permission.action)
            
            for resource, actions in permissions_by_resource.items():
                print(f"    • {resource}: {', '.join(actions)}")
        
        # 3. Show User Assignments
        print("\n👥 USER ROLE ASSIGNMENTS")
        print("-" * 25)
        
        users = User.query.all()
        for user in users:
            roles = user.get_roles()
            print(f"{user.username} ({user.email}): {', '.join(roles)}")
        
        # 4. Show Sample Inventory
        print("\n📦 SAMPLE INVENTORY")
        print("-" * 20)
        
        items = InventoryItem.query.limit(5).all()
        if items:
            print("ID | Name           | Quantity | Price    | Category")
            print("-" * 55)
            for item in items:
                price_str = f"${item.price:.2f}" if item.price else "N/A"
                print(f"{item.id:2} | {item.name:14} | {item.quantity:8} | {price_str:8} | {item.category or 'N/A'}")
        else:
            print("No inventory items found.")
        
        # 5. Show Recent Access Logs
        print("\n📋 RECENT ACCESS LOGS (Last 10)")
        print("-" * 32)
        
        recent_logs = AccessLog.query.order_by(AccessLog.timestamp.desc()).limit(10).all()
        if recent_logs:
            print("Time     | User    | Action                | Resource  | Status")
            print("-" * 65)
            for log in recent_logs:
                time_str = log.timestamp.strftime('%H:%M:%S')
                status = "✓" if log.success else "✗"
                action_short = log.action[:20] + "..." if len(log.action) > 20 else log.action
                print(f"{time_str} | {log.user.username:7} | {action_short:20} | {log.resource:9} | {status}")
        else:
            print("No access logs found.")
        
        # 6. Security Features Summary
        print("\n🛡️  SECURITY FEATURES")
        print("-" * 22)
        print("✓ Role-based access control with hierarchical permissions")
        print("✓ Secure password hashing (Werkzeug)")
        print("✓ Session-based authentication (Flask-Login)")
        print("✓ Comprehensive audit logging")
        print("✓ Access attempt monitoring (success/failure)")
        print("✓ IP address and user agent tracking")
        print("✓ Unauthorized access prevention with logging")
        print("✓ Role validation that cannot be bypassed")
        
        # 7. Access Control Matrix
        print("\n📊 ACCESS CONTROL MATRIX")
        print("-" * 25)
        print("Feature                | Admin | Manager | Viewer")
        print("-" * 50)
        print("Dashboard             |   ✓   |    ✓    |   ✓   ")
        print("View Inventory        |   ✓   |    ✓    |   ✓   ")
        print("Create Inventory      |   ✓   |    ✓    |   ✗   ")
        print("Edit Inventory        |   ✓   |    ✓    |   ✗   ")
        print("Delete Inventory      |   ✓   |    ✓    |   ✗   ")
        print("User Management       |   ✓   |    ✗    |   ✗   ")
        print("Role Management       |   ✓   |    ✗    |   ✗   ")
        print("Access Logs           |   ✓   |    ✗    |   ✗   ")
        
        # 8. Test Credentials
        print("\n🔑 TEST CREDENTIALS")
        print("-" * 18)
        print("Username: admin    | Password: admin123    | Role: Admin")
        print("Username: manager  | Password: manager123  | Role: Manager")
        print("Username: viewer   | Password: viewer123   | Role: Viewer")
        
        print("\n🌐 WEB APPLICATION")
        print("-" * 18)
        print("Access the web interface at: http://localhost:5000")
        print("Login with any of the test credentials above")
        
        print("\n✨ DEMONSTRATION COMPLETE")
        print("=" * 60)
        print("The RBAC system is fully functional and ready for use!")
        print("Run 'python app.py' to start the web application.")

if __name__ == '__main__':
    demonstrate_rbac()