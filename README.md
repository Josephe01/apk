# Advanced Inventory Management System

A comprehensive web-based inventory management system with live monitoring, real-time audit capabilities, and user accountability features.

## Features

### 🎯 Core Features
- **User Authentication & Role Management** - Admin, Manager, and User roles with appropriate permissions
- **Real-time Inventory Management** - Add, edit, delete, and track inventory items
- **Live Audit Sessions** - Conduct inventory audits with barcode scanning capability
- **WebSocket Real-time Updates** - Live monitoring banner during active audit sessions
- **Session Tracking & Reporting** - Comprehensive audit logs and session summaries
- **Export Functionality** - Generate PDF and CSV reports of audit sessions

### 🔍 Live Monitoring Features
- **Real-time Banner** - Shows active inventory checks to all users
- **Live Statistics** - Items scanned, discrepancies found, session duration
- **User Activity Tracking** - Log all user actions with timestamps
- **Notification System** - Real-time alerts for key events
- **Session Summaries** - Detailed reports for administrators

### 📊 Inventory Management
- **Item Management** - Complete CRUD operations for inventory items
- **Barcode Support** - Scan or manually enter barcodes/SKUs
- **Discrepancy Tracking** - Automatic calculation of quantity differences
- **Search & Filtering** - Find items by name, category, or discrepancy status
- **Location Tracking** - Track where items are stored

### 🔐 Security & Access Control
- **Role-based Access** - Different permissions for different user roles
- **Session Management** - Secure user authentication with Flask-Login
- **Audit Logging** - Complete trail of all inventory changes

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd apk
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Access the application at `http://localhost:5000`

### Default Credentials
- **Username**: `admin`
- **Password**: `admin123`

## Usage

### Starting an Audit Session
1. Log in to the system
2. Click "Start Now" on the dashboard or use the navigation menu
3. Use the barcode scanner or manually enter SKU/barcode
4. Enter the actual quantity found
5. Click "Scan" to record the item
6. Complete the session when finished

### Managing Inventory
1. Navigate to the "Inventory" section
2. Use search and filters to find specific items
3. Add new items using the "Add Item" button
4. Edit existing items using the action buttons
5. View discrepancies in the status columns

### Generating Reports
1. Complete an audit session
2. Navigate to the "Reports" section
3. Select the desired session
4. Choose PDF or CSV export format
5. Download the generated report

## System Architecture

### Backend Components
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **Flask-SocketIO** - WebSocket support for real-time updates
- **Flask-Login** - User session management
- **ReportLab** - PDF report generation

### Database Schema
- **Users** - User accounts and roles
- **InventoryItem** - Product catalog
- **AuditSession** - Audit session tracking
- **AuditLog** - Detailed action logs

### Frontend Components
- **Bootstrap 5** - Responsive UI framework
- **Socket.IO Client** - Real-time WebSocket communication
- **Vanilla JavaScript** - Client-side functionality

## API Endpoints

### Authentication
- `POST /login` - User login
- `GET /logout` - User logout

### Inventory Management
- `GET /inventory` - View inventory items
- `POST /api/item` - Add new item
- `GET /api/item/<id>` - Get item details
- `PUT /api/item/<id>` - Update item
- `DELETE /api/item/<id>` - Delete item

### Audit Sessions
- `POST /start_audit` - Start new audit session
- `GET /audit/<session_id>` - Audit interface
- `POST /api/scan` - Scan item during audit
- `POST /api/session/<id>/end` - End audit session
- `GET /api/session/<id>/export` - Export session report

### WebSocket Events
- `audit_started` - New audit session began
- `audit_updated` - Session statistics changed
- `audit_completed` - Session finished
- `item_scanned` - Item was scanned
- `discrepancy_found` - Quantity discrepancy detected

## Key Features Implemented

### ✅ User Activity Tracking
- All user actions are logged with timestamps
- Session start/end times recorded
- Audit trail for inventory changes

### ✅ Live Monitoring Window
- Real-time banner displayed to all users during active audits
- Dynamic updates via WebSocket connections
- Session progress tracking (items scanned, discrepancies)

### ✅ Session Summary for Admins
- Detailed session reports with user info, timestamps, and statistics
- Export functionality (PDF/CSV)
- Comprehensive audit logs

### ✅ Notifications
- Real-time notifications for session events
- Discrepancy alerts
- Session completion notifications

### ✅ Role-based Access Control
- Admin: Full system access
- Manager: Inventory management and audit control
- User: Basic inventory viewing and audit participation

## Screenshots

The system includes:
1. **Login Page** - Secure authentication
2. **Dashboard** - Overview with quick actions and statistics
3. **Inventory Management** - Complete item management interface
4. **Live Audit Interface** - Real-time scanning and tracking
5. **Live Monitoring Banner** - Visible across all pages during audits

## Technical Notes

### WebSocket Implementation
- Uses Flask-SocketIO for real-time communication
- Broadcasting to all connected users
- Automatic reconnection handling

### Database Design
- SQLite for development (easily changeable to PostgreSQL/MySQL)
- Proper foreign key relationships
- Optimized queries for performance

### Security Considerations
- Password hashing with Werkzeug
- Session-based authentication
- Role-based access control
- Input validation and sanitization

## Development

### Running in Development Mode
```bash
python app.py
```
The application will run with debug mode enabled on `http://localhost:5000`.

### Database Initialization
The application automatically creates the database and adds sample data on first run.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the repository.