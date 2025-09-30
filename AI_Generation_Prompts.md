# AI Generation Prompts for Laravel Inventory Project

This file contains a complete set of prompts for AI (Copilot, ChatGPT, etc) to generate the full Laravel inventory project as described in `PROJECT_SPEC.md`.

---

## 1. Project Initialization

> Create a new Laravel 10 project named `apk`.

---

## 2. Database Migrations

> Generate Laravel migration files for all tables described in PROJECT_SPEC.md, using the detailed schema for field types, constraints, relationships, and best practices.

### Table-by-table prompts:

#### Users Table
> Generate a Laravel migration for the `users` table:
> - id: BIGINT, primary key, auto-increment
> - name: VARCHAR(100), required
> - email: VARCHAR(150), unique, required
> - password: VARCHAR(255), required
> - role: ENUM('admin', 'manager', 'user'), default 'user', required
> - created_at, updated_at: TIMESTAMP

#### InventoryItems Table
> Generate a Laravel migration for the `inventory_items` table:
> - id: BIGINT, primary key, auto-increment
> - name: VARCHAR(100), required
> - sku: VARCHAR(50), unique, required
> - barcode: VARCHAR(100), unique, nullable
> - expected_quantity: INT, default 0, required
> - actual_quantity: INT, default 0, required
> - category: VARCHAR(50), required
> - location: VARCHAR(100), nullable
> - created_at, updated_at: TIMESTAMP

#### AuditSessions Table
> Generate a Laravel migration for the `audit_sessions` table:
> - id: BIGINT, primary key, auto-increment
> - session_id: UUID, unique, required
> - user_id: BIGINT, foreign key to `users.id`, required
> - start_time: TIMESTAMP, required
> - end_time: TIMESTAMP, nullable
> - status: ENUM('active', 'completed', 'cancelled'), default 'active', required
> - items_scanned: INT, default 0, required
> - discrepancies_found: INT, default 0, required
> - notes: TEXT, nullable
> - created_at, updated_at: TIMESTAMP

#### AuditLogs Table
> Generate a Laravel migration for the `audit_logs` table:
> - id: BIGINT, primary key, auto-increment
> - session_id: BIGINT, foreign key to `audit_sessions.id`, required
> - user_id: BIGINT, foreign key to `users.id`, required
> - item_id: BIGINT, foreign key to `inventory_items.id`, required
> - action: ENUM('scan', 'adjust', 'note'), required
> - old_quantity: INT, nullable
> - new_quantity: INT, nullable
> - discrepancy: INT, default 0, required
> - timestamp: TIMESTAMP, required
> - notes: TEXT, nullable

#### Settings Table
> Generate a Laravel migration for the `settings` table:
> - id: BIGINT, primary key, auto-increment
> - user_id: BIGINT, foreign key to `users.id`, required
> - theme: ENUM('light', 'dark', 'blue'), default 'light', required
> - icon_set: ENUM('fontawesome', 'bootstrap'), default 'fontawesome', required
> - created_at, updated_at: TIMESTAMP

---

## 3. Eloquent Models

> Generate Eloquent models for each table, including fillable fields, relationships, and relevant casts.

---

## 4. Model Relationships

> Add correct `hasMany`, `belongsTo`, and other relationships between models as described in the schema in PROJECT_SPEC.md.

---

## 5. Seeders and Factories

> Generate Laravel factories and seeders for initial test data for all tables.

---

## 6. Controllers

> Generate controllers for Inventory, Audit, Dashboard, Settings, and Auth, each with full CRUD methods and resource route conventions.

---

## 7. Requests & Validation

> Generate Form Request classes for each resource, with validation rules based on the business logic and database constraints.

---

## 8. Blade Views

> Generate Blade templates for each listed view (`dashboard`, `inventory/index`, `audit/index`, `settings/index`, `auth/login`, `layouts/base`), with navigation and forms matching the spec.

---

## 9. JavaScript & CSS Assets

> Generate `public/js/app.js` for AJAX, real-time features, and UI interactivity.
> Generate `public/css/style.css` for base styles.

---

## 10. API Routes

> Generate RESTful API routes for each resource (inventory, audits, reports, settings) as described in PROJECT_SPEC.md.

---

## 11. API Controllers

> Generate API controllers for all endpoints, handling requests, responses, and resource formatting.

---

## 12. Authentication & User Roles

> Set up authentication (using Laravel Breeze/Jetstream) and implement role-based access control in controllers and middleware.

---

## 13. Notifications & Real-Time

> Set up broadcasting (e.g., Pusher) and generate code for sending notifications on audit progress and discrepancies.

---

## 14. README & Documentation

> Generate a README.md containing setup instructions, feature list, API documentation (sample requests/responses), and migration usage.

---

## 15. Testing

> Generate PHPUnit tests for migrations, models, controllers, and API endpoints.

---

## 16. .env Example

> Generate an example `.env` file with recommended settings for local development.

---

## 17. Additional Features (Optional)

> Generate migration/model/controller for suppliers, attachments, notifications, etc. (if you decide to add these).

---

You can use these prompts step-by-step or all together for AI-driven full project generation.