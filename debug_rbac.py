#!/usr/bin/env python3
"""
Debug RBAC functionality
"""

from app import app, User, Role

def debug_user_roles():
    """Debug user role assignments"""
    with app.app_context():
        users = User.query.all()
        for user in users:
            print(f"User: {user.username}")
            print(f"  Roles: {user.get_roles()}")
            print(f"  has_role('Admin'): {user.has_role('Admin')}")
            print(f"  has_role('Manager'): {user.has_role('Manager')}")
            print(f"  has_role('Viewer'): {user.has_role('Viewer')}")
            print()

if __name__ == '__main__':
    debug_user_roles()