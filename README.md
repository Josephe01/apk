# Advanced Inventory Management System

A web-based inventory management system with robust audit capabilities, real-time notifications, user accountability, and comprehensive reporting. Built using Laravel (PHP), MySQL, and Blade.

## Features

### Core Features
- **User Authentication & Role Management:** Admin, Manager, and User roles with secure permissions, password hashing, login throttling, Multi-Factor Authentication (MFA), and CAPTCHA.
- **Inventory Management:** CRUD operations for inventory items; fields include Name, SKU, Barcode, Category, Location, Expected Quantity, Actual Quantity.
- **Location Management:** Define/manage locations (warehouses, aisles, shelves), assign products, and track movements.
- **Bulk Operations:** Add, update, or delete multiple items at once.
- **Product Images:** Upload, resize, and store images with default placeholders.
- **Barcode Scanning Integration:** Use mobile cameras or hardware scanners to lookup items.
- **Stock Adjustment Logs:** Track changes to inventory quantities.
- **Multi-Warehouse Support:** Track inventory across multiple warehouses.
- **Real-Time Stock Sync:** Synchronize stock levels across sessions.
- **Batch Import/Export:** Import/export inventory data from/to CSV/Excel.
- **Audit and Discrepancy Reports:** Generate reports for mismatched quantities and audit summaries.
- **Role-Based Inventory Access:** Permissions according to user roles.

### Stock Audit
- Compare actual quantities with expected values.
- Barcode scanning for fast item identification.
- Automatic logging of discrepancies with details.
- Detailed audit reports (PDF/CSV), session summaries, real-time audit progress, and audit logs.

### Real-Time Notifications
- Low stock alerts, audit progress, and item changes using Laravel Echo and Pusher.

### Reports & Logs
- Exportable PDF and CSV reports.
- Filterable audit session logs.

### API
- RESTful endpoint for barcode/SKU search.
- Dynamic product detail responses.

## Technology Stack

- **Backend:** PHP (Laravel Framework)
- **Database:** MySQL
- **Templating Engine:** Blade
- **Frontend:** HTML5, CSS3, Bootstrap, optional JavaScript libraries
- **Real-Time:** Laravel Echo, Pusher/WebSockets
- **PDF Export:** dompdf
- **Deployment:** Docker & Docker Compose (Unraid server)

## HTTPS Integration (Proposed Solution)

**Steps:**
1. Integrate HTTPS using a reverse proxy (Nginx or Apache).
2. Obtain and install an SSL/TLS certificate (Let's Encrypt or commercial CA).
3. Redirect all HTTP traffic to HTTPS.
4. Update application settings and documentation to reflect HTTPS usage.
5. Test all features—including real-time updates—under HTTPS.

**Benefits:**
- Encrypts communication, protecting sensitive data.
- Increases user trust, avoids browser warnings.
- Meets best practices and compliance for user data protection.

**Notes:**
- Additional configuration may be needed for WebSockets over HTTPS.
- Replace default credentials before production deployment.

## Installation

### Prerequisites
- Docker & Docker Compose (recommended)
- PHP 8.1+ (if installing without Docker)
- MySQL 8+ (if installing without Docker)
- Node.js & npm (for frontend assets)

### Quick Start (Docker)
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd apk
   ```
2. Copy environment file and set parameters:
   ```bash
   cp .env.example .env
   # Edit .env to set database and mail settings
   ```
3. Build and start containers:
   ```bash
   docker-compose up -d
   ```
4. Run database migrations and seed data:
   ```bash
   docker-compose exec app php artisan migrate --seed
   ```
5. Access the app at `http://localhost:8000` (or `https://localhost:8000` if HTTPS configured)

### Manual Installation (without Docker)
1. Install PHP, MySQL, Composer, and Node.js.
2. Clone repo, set up `.env`, install dependencies:
   ```bash
   composer install
   npm install && npm run build
   php artisan migrate --seed
   php artisan serve
   ```
3. Access at `http://localhost:8000`

### Default Credentials
- **Username:** `admin@example.com`
- **Password:** `admin123`  
*Change these before production!*

## Usage

- **Inventory:** Add, edit, delete, and search inventory items. Assign items to locations.
- **Audit:** Start audit sessions, scan barcodes, enter actual quantities, log discrepancies.
- **Reports:** Generate and export PDF/CSV audit summaries.
- **Notifications:** Receive real-time alerts for inventory events.
- **API:** Use barcode/SKU endpoints to search for products.

## System Architecture

- **Backend:** Laravel (MVC), MySQL, Redis (optional for queue/cache)
- **Frontend:** Blade, Bootstrap, JS libraries
- **Real-Time:** Laravel Echo + Pusher/WebSockets
- **PDF/CSV:** dompdf, Laravel export tools
- **Deployment:** Docker containers

## API Endpoints (Sample)
- `POST /api/login` - Authenticate user
- `GET /api/inventory` - List items
- `POST /api/inventory` - Add item
- `PUT /api/inventory/{id}` - Update item
- `DELETE /api/inventory/{id}` - Delete item
- `POST /api/audit/start` - Start audit session
- `POST /api/audit/scan` - Scan item during audit
- `GET /api/audit/report/{id}` - Export audit report

## Security Considerations

- Password hashing, session management, MFA, CAPTCHA
- Role-based access control
- Input validation and sanitization
- Audit logging of inventory changes and user actions

## Development

- **Run Tests:**  
  ```bash
  php artisan test
  ```
- **Build Frontend:**  
  ```bash
  npm run build
  ```
- **Database Seeding:**  
  ```bash
  php artisan db:seed
  ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License

## Support

For support and questions, please open an issue in the repository.
