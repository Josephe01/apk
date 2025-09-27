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
   - Fields: Name, SKU, Barcode, Category, Location, Expected Quantity, Actual Quantity.
   - **Location Management**:
     - Define and manage locations (e.g., warehouses, aisles, shelves).
     - Assign products to specific locations.
     - Reassign and track product movements between locations.
   - Advanced Search and Filters:
     - Search by name, SKU, barcode, category, or location.
   - Bulk Operations:
     - Add, update, or delete multiple items at once.
   - **Product Images**:
     - Upload, resize, and store product images.
     - Ensure uniform dimensions and optimized file sizes.
     - Default placeholder image for products without an image.
   - **Barcode Scanning Integration**:
     - Use mobile phone cameras or hardware barcode scanners.
     - Search database for product details by scanning barcodes.
   - Stock Adjustment Logs:
     - Log and track changes to inventory quantities.
   - Multi-Warehouse Support:
     - Track inventory across multiple warehouses.
   - Real-Time Stock Sync:
     - Synchronize stock levels in real time across sessions.
   - Batch Import/Export:
     - Import inventory data from CSV/Excel files.
     - Export inventory for external use.
   - Audit and Discrepancy Reports:
     - Generate reports for mismatched quantities and audit summaries.
   - Role-Based Inventory Access:
     - Users with different roles have specific permissions (e.g., read-only for regular users).

3. **Stock Audit**:
   - Conduct stock audits to compare **actual quantities** with **expected quantities**.
   - Use barcode scanning (mobile or hardware) to quickly identify products.
   - Log discrepancies automatically:
     - Include details such as product, location, and quantity differences.
   - Generate detailed audit reports:
     - Session summaries with timestamps, user activity, and results.
     - Export reports in PDF or CSV formats.
   - Real-time audit progress tracking:
     - Display scanned items, discrepancies found, and session duration.
   - Maintain an **audit log** for accountability:
     - Track actions and changes made during the audit.

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

6. **Barcode Search API**:
   - RESTful endpoint for searching inventory by barcode or SKU.
   - Return product details dynamically.

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
   - Add product image upload and barcode scanning.

3. **Location Management**:
   - Create migrations for the `locations` table.
   - Add functionality for assigning products to locations.
   - Track product movements between locations.

4. **Stock Audit**:
   - Develop dedicated UI for stock audits.
   - Create backend logic for comparing actual and expected quantities.
   - Implement automatic logging of discrepancies.
   - Add real-time progress tracking for audits.
   - Generate detailed audit reports (PDF/CSV).

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

4. **Barcode Scanning Integration**:
   - Use QuaggaJS for mobile phone camera scanning.
   - Support hardware scanners for seamless integration.

5. **API for Barcode Search**:
   - Add a RESTful API endpoint for barcode-based searches.
   - Return product details dynamically.

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