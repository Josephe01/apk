# Advanced Inventory Management System

## Project Overview
The Advanced Inventory Management System is a web-based application designed to manage inventory efficiently while providing robust audit capabilities, real-time notifications, and reporting functionality. The system supports role-based user authentication and allows administrators to monitor and control inventory with ease.

---

## Technology Stack
### Backend
- **Language**: PHP
- **Framework**: Laravel
- **Database**: MySQL
- **Templating Engine**: Blade (Laravel's templating system)

### Frontend
- **HTML/CSS**: For structure and design.
- **Bootstrap**: For responsiveness and styling.
- **Optional Enhancements**: Integration of JavaScript libraries for dynamic interactivity.

### Deployment
- **Docker**: For containerized deployment on an Unraid server.
- **Docker Compose**: To manage Laravel, MySQL, and additional services like Redis if needed.

---

## Features
### Core Features
1. **User Authentication**:
   - Login/Logout functionality.
   - Role-based permissions (admin, manager, user).
   - Password hashing and security.
   - Login throttling to prevent brute force attacks.
   - Multi-Factor Authentication (MFA) for added security.
   - CAPTCHA verification on failed login attempts.
   - Email notifications for suspicious login activity.

2. **Inventory Management**:
   - CRUD operations for inventory items.
   - Fields: Name, SKU, Category, Location, Expected Quantity, Actual Quantity.
   - Advanced Search and Filters:
     - Search by name, SKU, category, location, or low stock status.
   - Bulk Operations:
     - Add, update, or delete multiple items at once.
   - Stock Adjustment Logs:
     - Log and track changes to inventory quantities.
   - Multi-Warehouse Support:
     - Track inventory across multiple warehouses.
   - Barcode Scanning Integration:
     - Add, look up, and adjust items using barcode scanners.
   - Real-Time Stock Sync:
     - Synchronize stock levels in real time across sessions.
   - Batch Import/Export:
     - Import inventory data from CSV/Excel files.
     - Export inventory for external use.
   - Audit and Discrepancy Reports:
     - Generate reports for mismatches and summaries of audits.
   - Role-Based Inventory Access:
     - Users with different roles have specific permissions (e.g., read-only for regular users).

### Additional Features
3. **Real-Time Notifications**:
   - Low stock alerts.
   - Audit progress updates.
   - Notifications for changes (e.g., new items added).

4. **Exportable Reports**:
   - Generate PDF/CSV reports for inventory and audit logs.
   - Include summary statistics in reports.

5. **Audit Session Logs**:
   - Store logs of actions taken during audits.
   - Filter logs by date, user, or action.

---

## Implementation Plan
### Phase 1: Project Initialization
- Set up Laravel with MySQL.
- Configure `.env` for database connection.
- Install necessary Laravel libraries (e.g., Laravel Breeze for authentication).

### Phase 2: Core Features
1. **User Authentication**:
   - Create migrations for the `users` table.
   - Implement login/logout and role-based permissions.
   - Add login throttling, MFA, and CAPTCHA verification.

2. **Inventory Management**:
   - Create migrations for the `inventory_items` table.
   - Implement CRUD operations via controllers and Blade templates.
   - Add advanced search, filters, and bulk operations.
   - Implement stock adjustment logs and multi-warehouse support.

### Phase 3: Additional Features
1. **Real-Time Notifications**:
   - Implement WebSocket-based notifications (Laravel Echo + Pusher).
   - Add frontend support for displaying notifications.

2. **Exportable Reports**:
   - Use `dompdf` for PDF generation.
   - Use Laravel’s built-in CSV tools for exporting data.

3. **Audit Session Logs**:
   - Create a dedicated log viewer in the admin panel.
   - Enable filtering and searching functionality.

### Phase 4: Deployment
- Create a `Dockerfile` and `docker-compose.yml` for deployment.
- Test the system on your Unraid server.
- Set up SSL (if required) using Nginx or Traefik.

---

## Future Enhancements
- Add multi-language support.
- Integrate OAuth for third-party logins (e.g., Google, Facebook).
- Implement advanced reporting with graphs and charts.

---

## Timeline
1. **Phase 1 (1 Week)**: Project setup and database migrations.
2. **Phase 2 (2–3 Weeks)**: Implement core features.
3. **Phase 3 (2 Weeks)**: Add additional features.
4. **Phase 4 (1 Week)**: Deployment and testing.

---

## Contributors
- **Owner**: Josephe01