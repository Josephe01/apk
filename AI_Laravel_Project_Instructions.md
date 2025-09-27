# Laravel Inventory Management System - AI Project Instructions

This checklist is designed for AI systems or automation to **fully generate a Laravel-based inventory management system**.  
Use the commands, structure, and prompts below to build, scaffold, and configure your application from scratch.

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

## 1. Project Initialization

**Command:**
```bash
composer create-project laravel/laravel apk
cd apk
```

---

## 2. Directory Structure

**Ensure the following structure:**
- Models: `/app/Models/`
- Controllers: `/app/Http/Controllers/`
- Views (Blade): `/resources/views/`
- Static Assets: `/public/js/`, `/public/css/`
- Routes: `/routes/web.php`, `/routes/api.php`
- Environment: `.env`

---

## 3. Generate Models and Migrations

**Commands:**
```bash
php artisan make:model InventoryItem -m
php artisan make:model AuditSession -m
php artisan make:model AuditLog -m
php artisan make:model Settings -m
```

**AI Model Prompts:**
- *"Generate a Laravel model for InventoryItem with fields: name, sku, barcode, expected_quantity, actual_quantity, category, location."*
- *"Generate a Laravel model for AuditSession with fields: session_id, user_id, start_time, end_time, status, items_scanned, discrepancies_found, notes."*
- *"Generate a Laravel model for AuditLog with fields: session_id, user_id, item_id, action, old_quantity, new_quantity, discrepancy, timestamp, notes."*
- *"Generate a Laravel model for Settings with fields: user_id, theme, icon_set, created_at, updated_at."*

---

## 4. Generate Controllers

**Commands:**
```bash
php artisan make:controller InventoryController --resource
php artisan make:controller AuditController
php artisan make:controller DashboardController
php artisan make:controller SettingsController
php artisan make:controller Auth/LoginController
```

**AI Controller Prompts:**
- *"Create a resource controller for InventoryItem: index, create, store, show, edit, update, destroy."*
- *"Create a controller for AuditSession to start, scan, end sessions, and export reports."*
- *"Create a DashboardController that loads recent inventory and active sessions."*
- *"Create a SettingsController to handle theme/icon preferences."*
- *"Create an Auth/LoginController for login/logout functionality."*

---

## 5. Generate Blade Views (Templates)

**AI View Prompts:**
- *"Generate a Blade template for the dashboard, showing recent items and active sessions."*
- *"Generate a Blade template for inventory management with table, search/filter, add/edit/delete modals."*
- *"Generate a Blade template for audit session: scanning interface, stats, session summary."*
- *"Generate a Blade template for settings page: theme selection, icon set."*
- *"Generate a Blade template for login form with error handling."*

---

## 6. Static Assets

**Instructions:**
- Place main JS in `/public/js/app.js` and main CSS in `/public/css/style.css`.
- Reference assets in Blade views using `{{ asset('js/app.js') }}` and `{{ asset('css/style.css') }}`.

**AI Asset Prompts:**
- *"Generate a JavaScript file for inventory management, handling AJAX requests and real-time updates using Laravel Echo."*
- *"Generate a CSS file for dashboard, tables, buttons, and audit banners."*

---

## 7. Routing

**Define routes in `routes/web.php` and `routes/api.php`:**

**AI Route Prompts:**
- *"Create web routes for dashboard, inventory, audit, settings, and authentication using Laravel's Route facade."*
- *"Create API routes for inventory CRUD, audit actions, and report export."*

**Sample web.php:**
```php
Route::get('/', [DashboardController::class, 'index'])->name('dashboard');
Route::resource('inventory', InventoryController);
Route::get('/audit/{session}', [AuditController::class, 'show'])->name('audit.show');
Route::post('/audit/start', [AuditController::class, 'start'])->name('audit.start');
Route::post('/audit/scan', [AuditController::class, 'scan'])->name('audit.scan');
Route::post('/audit/{session}/end', [AuditController::class, 'end'])->name('audit.end');
Route::get('/settings', [SettingsController::class, 'index'])->name('settings.index');
Route::post('/settings', [SettingsController::class, 'update'])->name('settings.update');
```

---

## 8. Authentication

**Instructions:**
- Use Laravel Breeze or Fortify for authentication scaffolding.

**AI Auth Prompts:**
- *"Set up Laravel authentication with registration, login, logout, password reset."*

---

## 9. Database Setup

**Commands:**
```bash
php artisan migrate
php artisan db:seed
```

**AI Data Prompts:**
- *"Generate seeders for default admin user and sample inventory items."*

---

## 10. Real-Time Features

**Instructions:**
- Use Laravel Echo with Pusher for notifications and audit session updates.
- Configure Pusher keys in `.env`.

**AI Real-Time Prompts:**
- *"Generate events and listeners for real-time audit progress and notifications using Laravel Echo."*

---

## 11. Environment Configuration

**Instructions:**
- Set DB, mail, and Pusher credentials in `.env`.

**AI Env Prompts:**
- *"Configure .env for MySQL database, mail, and Pusher (or other broadcasting service)."*

---

## 12. Documentation

**Instructions:**
- Update `README.md` with setup, usage, and API documentation.

**AI Doc Prompts:**
- *"Generate a README.md with installation, features, usage, and API endpoint documentation for this Laravel inventory system."*

---

## 13. General Conventions

- Use Laravel Eloquent for models.
- Use Blade templates for views.
- Place assets in `/public`.
- Use RESTful routes for APIs.
- Use Laravel’s built-in middleware for authentication and authorization.

---

## 14. Example AI Prompt (for any task)

*"Generate a Laravel controller named InventoryController implementing CRUD methods and returning Blade views for each action."*

*"Produce a Blade template for inventory listing with search and filter controls."*

*"Write the migration file for AuditSession as per the provided fields."*

---

## 15. Final Checklist

- [ ] Project initialized with Laravel
- [ ] Models, controllers, migrations, seeders generated
- [ ] Blade templates created
- [ ] JS/CSS assets in place
- [ ] Routes defined
- [ ] Auth implemented
- [ ] Database migrated/seeded
- [ ] Real-time events configured
- [ ] Environment variables set
- [ ] Documentation updated

---

**When ready, AI/automation should follow this script and use the prompts to generate all code, configs, and docs for the project.