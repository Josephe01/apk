# Inventory Management System - Project Specification

This file is a living blueprint for the whole project.  
Every feature, module, architectural decision, and requirement discussed is tracked here.  
Whenever you add or change something, update this file so all planning is preserved for future AI-driven code generation.

---

## Features & Requirements

### 1. Authentication & User Roles
- User registration, login, logout, password reset
- Roles: admin, manager, user
- Role-based access control for features

### 2. Inventory Management
- Add/edit/delete inventory items
- Item fields: name, SKU, barcode, expected_quantity, actual_quantity, category, location
- Search and filter inventory
- Bulk import/export (CSV)

### 3. Audit Sessions
- Start, pause, complete inventory audits
- Scanning interface for barcode/SKU
- Track items scanned, discrepancies, completion rate
- Audit logs per session

### 4. Reports & Exports
- Generate PDF and CSV reports for audit sessions
- Downloadable summaries

### 5. System Settings
- Change theme (light/dark)
- Choose icon set
- Save user preferences

### 6. Real-Time Notifications
- Live updates on audit progress, item scans, discrepancies
- Push notifications via WebSockets

### 7. Dashboard
- Show recent inventory updates
- List active audit sessions
- Quick links to main actions

### 8. Security
- Password hashing, session management
- Input validation/sanitization
- Audit logging

### 9. API Endpoints
- RESTful API for inventory, audits, reports, settings

### 10. Documentation
- README with setup, usage, and API docs
- Inline code comments

---

## Modularity & Architecture

- Separate controllers for each major module (Inventory, Audit, Dashboard, Settings, Auth)
- Blade templates for all views
- JS/CSS assets in public directory
- Use Laravel Eloquent models and migrations for DB
- Configurable via .env
- Extensible to add modules (e.g., suppliers, attachments) in future

---

## Database Schema

### Users
- id: BIGINT, primary key, auto-increment
- name: VARCHAR(100), required
- email: VARCHAR(150), unique, required
- password: VARCHAR(255), required (hashed)
- role: ENUM('admin', 'manager', 'user'), default 'user', required
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

### InventoryItems
- id: BIGINT, primary key, auto-increment
- name: VARCHAR(100), required
- sku: VARCHAR(50), unique, required
- barcode: VARCHAR(100), unique, nullable
- expected_quantity: INT, default 0, required
- actual_quantity: INT, default 0, required
- category: VARCHAR(50), required
- location: VARCHAR(100), nullable
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

### AuditSessions
- id: BIGINT, primary key, auto-increment
- session_id: UUID, unique, required
- user_id: BIGINT, foreign key → users.id, required
- start_time: TIMESTAMP, required
- end_time: TIMESTAMP, nullable
- status: ENUM('active', 'completed', 'cancelled'), default 'active', required
- items_scanned: INT, default 0, required
- discrepancies_found: INT, default 0, required
- notes: TEXT, nullable
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

### AuditLogs
- id: BIGINT, primary key, auto-increment
- session_id: BIGINT, foreign key → audit_sessions.id, required
- user_id: BIGINT, foreign key → users.id, required
- item_id: BIGINT, foreign key → inventory_items.id, required
- action: ENUM('scan', 'adjust', 'note'), required
- old_quantity: INT, nullable
- new_quantity: INT, nullable
- discrepancy: INT, default 0, required
- timestamp: TIMESTAMP, required
- notes: TEXT, nullable

### Settings
- id: BIGINT, primary key, auto-increment
- user_id: BIGINT, foreign key → users.id, required
- theme: ENUM('light', 'dark', 'blue'), default 'light', required
- icon_set: ENUM('fontawesome', 'bootstrap'), default 'fontawesome', required
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

#### *Extend as needed:*
- Notifications
- Attachments
- API tokens

**Relationships:**  
- User has many AuditSessions, AuditLogs, Settings  
- AuditSession has many AuditLogs  
- InventoryItem has many AuditLogs

**Laravel Migration Notes:**
- Use `$table->bigIncrements('id')` for primary keys.
- Use `$table->foreignId('user_id')->constrained()` for relationships.
- Use `$table->enum('role', ['admin','manager','user'])` for roles.
- Use `$table->uuid('session_id')->unique()` for UUIDs.
- Use `$table->string('sku', 50)->unique()` etc. for unique fields.
- Use `$table->timestamps()` for created_at/updated_at.

---

## API Endpoints (Sample)

- `POST /api/login` - Authenticate user
- `GET /api/inventory` - List items
- `POST /api/inventory` - Add item
- `PUT /api/inventory/{id}` - Update item
- `DELETE /api/inventory/{id}` - Delete item
- `POST /api/audit/start` - Start audit session
- `POST /api/audit/scan` - Scan item during audit
- `GET /api/audit/report/{id}` - Export audit report

---

## Blade Views Needed

- layouts/base.blade.php
- dashboard.blade.php
- inventory/index.blade.php
- audit/index.blade.php
- settings/index.blade.php
- auth/login.blade.php

---

## JS/CSS Assets

- public/js/app.js (AJAX, real-time, UI)
- public/css/style.css (main styles)

---

## Prompts for AI Code Generation

- "Generate Laravel migration files for each table above, including field types, constraints, relationships, and indexes."
- "Create InventoryController with CRUD methods."
- "Produce Blade template for inventory listing with search and filter controls."
- "Create DashboardController to load recent items and active sessions."
- "Write JS for inventory management and real-time audit updates."
- "Generate README.md with setup, features, and API docs."

---

## User Stories / Use Cases

- As an admin, I want to add/edit/delete inventory items.
- As a manager, I want to start and complete audit sessions.
- As a user, I want real-time notifications when audits are running.
- As any user, I want to change my theme preference.
- As an admin, I want to export audit reports for compliance.
- As a developer, I want RESTful API endpoints to integrate with other systems.

---

## TODOs / Open Questions / Future Plans

- Add supplier management module?
- Add image/attachment support for inventory items?
- Integrate with external barcode scanning hardware?
- Add more granular permissions/roles?

---

**Whenever you discuss a new feature or decision, update this file!  
Your AI can always use this as the source of truth for generating the whole system.