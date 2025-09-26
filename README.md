# Advanced APK Management System

A comprehensive web-based application management system with advanced course management, dynamic theme customization, and real-time monitoring capabilities.

## 🚀 New Features

### Course Management System
- **Full CRUD Operations**: Create, read, update, and delete courses
- **Advanced Search & Filtering**: Filter by status, department, and search by name/code
- **Export Functionality**: Export course data in JSON or CSV formats
- **Enrollment Tracking**: Monitor course capacity and enrollment numbers
- **Metadata Support**: Store additional course information with JSON fields

### Dynamic Theme & Icon Customization
- **Theme Management**: Create and manage custom themes with live preview
- **User Preferences**: Individual user settings for themes, font sizes, and accessibility
- **Accessibility Features**: High contrast mode, adjustable font sizes, dark mode
- **Real-time Updates**: Instant theme application via WebSocket connections
- **Pre-built Themes**: Default, Dark, Professional, and High Contrast themes

### Enhanced UI/UX
- **Modern Dashboard**: Quick access cards for all major features
- **Responsive Design**: Mobile-friendly interface with Bootstrap 5
- **Real-time Notifications**: Live updates for system events
- **Advanced Analytics**: System health monitoring and usage statistics

## Features

### 🎯 Core Features
- **Role-Based Access Control (RBAC)**: Admin, Manager, and User roles with appropriate permissions
- **Course Management**: Full lifecycle management of courses with detailed metadata
- **Theme Customization**: Comprehensive theming system with live preview
- **User Preferences**: Personalized settings for optimal user experience
- **Real-time Monitoring**: Live updates and notifications via WebSocket
- **Export/Import**: Multiple format support for data exchange

### 🔍 Live Monitoring Features
- **Live Audit Banner**: Real-time display of active audit sessions
- **WebSocket Integration**: Instant updates across all connected users
- **Session Tracking**: Comprehensive audit trail with user accountability
- **System Health**: Performance monitoring and status indicators

### 📊 Inventory Management
- **Item Tracking**: Complete inventory lifecycle management
- **Barcode Scanning**: Integration-ready scanning capabilities
- **Discrepancy Detection**: Automatic identification of inventory issues
- **Reporting**: Comprehensive PDF and CSV report generation

### 🔐 Security & Access Control
- **User Authentication**: Secure login with session management
- **Permission System**: Granular access control based on user roles
- **Audit Logging**: Complete audit trail for compliance
- **Data Validation**: Input sanitization and validation throughout

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

### Course Management
1. Navigate to "Courses" in the main menu
2. Use "Add Course" to create new courses
3. Search and filter courses using the provided tools
4. Export course data using the Export dropdown
5. Edit or delete courses using the action buttons

### Theme Customization
1. Navigate to "Themes" in the main menu (Admin only)
2. Create custom themes with the theme editor
3. Use live preview to see changes in real-time
4. Set default themes for all users
5. Access personal preferences via the user menu

### Personal Preferences
1. Click the moon/sun icon to toggle dark mode
2. Use "Preferences" in the user dropdown for detailed settings
3. Adjust font size, contrast, and theme preferences
4. Changes apply instantly across the application

## Screenshots

### Enhanced Dashboard
![Dashboard](https://github.com/user-attachments/assets/13b9a997-b960-455b-93ad-fdd3be5385a0)
*New dashboard with course management and theme customization cards*

### Course Management Interface
![Course Management](https://github.com/user-attachments/assets/a54ddff1-e644-4cca-8f33-06e8007163e1)
*Complete course management with search, filtering, and export capabilities*

### Theme Management System
![Theme Management](https://github.com/user-attachments/assets/6577203f-1e9d-4988-850e-473291b43a32)
*Advanced theme editor with live preview and user preferences*

## System Architecture

### Backend Components
- **Flask** - Web framework with WebSocket support
- **SQLAlchemy** - Database ORM with JSON field support
- **Flask-SocketIO** - Real-time WebSocket communication
- **Flask-Login** - User session and authentication management
- **ReportLab** - PDF report generation

### Database Schema
- **Users** - User accounts with role-based permissions
- **Courses** - Course catalog with metadata support
- **Themes** - Theme configurations and user preferences
- **UserPreferences** - Individual user customizations
- **InventoryItem** - Product catalog (legacy)
- **AuditSession** - Audit session tracking (legacy)
- **AuditLog** - Detailed action logs (legacy)

### Frontend Components
- **Bootstrap 5** - Modern responsive UI framework
- **Socket.IO Client** - Real-time WebSocket communication
- **Vanilla JavaScript** - Client-side functionality with ES6+
- **CSS Custom Properties** - Dynamic theme application

## API Endpoints

### Course Management
- `GET /courses` - Course management interface
- `GET /api/courses` - List all courses
- `POST /api/courses` - Create new course
- `PUT /api/courses/<id>` - Update course
- `DELETE /api/courses/<id>` - Delete course
- `GET /api/courses/export` - Export courses (JSON/CSV)

### Theme Management
- `GET /themes` - Theme management interface
- `GET /api/themes` - List all themes
- `POST /api/themes` - Create custom theme
- `PUT /api/themes/<id>` - Update theme
- `POST /api/themes/<id>/set-default` - Set default theme

### User Preferences
- `GET /api/user/preferences` - Get user preferences
- `PUT /api/user/preferences` - Update user preferences

### Legacy Inventory System
- `GET /inventory` - View inventory items
- `POST /api/item` - Add new item
- `GET /api/item/<id>` - Get item details
- `PUT /api/item/<id>` - Update item
- `DELETE /api/item/<id>` - Delete item

### WebSocket Events
- `theme_updated` - Theme configuration changed
- `preferences_updated` - User preferences modified
- `audit_started` - New audit session began (legacy)
- `audit_updated` - Session statistics changed (legacy)
- `item_scanned` - Item was scanned (legacy)

## Key Features Implemented

### ✅ Course Management System
- Complete CRUD operations with validation
- Advanced search and filtering capabilities
- Export functionality (JSON/CSV formats)
- Enrollment tracking and capacity management
- Rich metadata support with JSON fields

### ✅ Dynamic Theme Customization
- Custom theme creation with live preview
- Color palette configuration
- Typography settings (font family, size)
- User-specific preference overrides
- Real-time theme application via WebSocket

### ✅ Accessibility Features
- High contrast mode for better visibility
- Adjustable font sizes (Small to X-Large)
- Dark mode with automatic icon switching
- ARIA labels and semantic HTML structure
- Keyboard navigation support

### ✅ Performance Optimization
- CSS custom properties for instant theme switching
- Lazy loading of theme assets
- Efficient WebSocket communication
- Optimized database queries with proper indexing

### ✅ Real-time Features
- WebSocket integration for live updates
- Instant theme application across all users
- Real-time preference synchronization
- Live system status monitoring

## Technical Notes

### Advanced Features
- **JSON Field Support**: Flexible metadata storage for courses
- **WebSocket Integration**: Real-time updates without page refresh
- **CSS Custom Properties**: Dynamic theme switching without reload
- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Accessibility Compliance**: WCAG 2.1 guidelines followed

### Security Considerations
- Role-based access control with proper authorization
- Input validation and sanitization throughout
- CSRF protection via Flask-WTF integration
- Secure session management with Flask-Login
- SQL injection prevention via SQLAlchemy ORM

### Database Design
- Normalized schema with proper foreign key relationships
- JSON fields for flexible metadata storage
- Indexing on frequently queried columns
- Support for both SQLite (development) and PostgreSQL (production)

## Development

### Running in Development Mode
```bash
python app.py
```
The application runs with debug mode enabled on `http://localhost:5000`.

### Database Initialization
The application automatically:
- Creates all database tables on first run
- Adds sample courses and themes
- Creates default admin user
- Initializes system preferences

### Adding New Themes
1. Access the Theme Management interface as admin
2. Use the theme editor with live preview
3. Configure colors, typography, and spacing
4. Test accessibility features
5. Set as default if desired

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper testing
4. Update documentation as needed
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For support and questions:
- Check the documentation above
- Review the code comments for implementation details
- Test the live demo features
- Submit issues via GitHub

---

**Version**: 2.0.0 - Course Management & Theme Customization Release