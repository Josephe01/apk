# Sample Data and Workflows

This section defines example data for initial seeding, and describes typical user workflows for the Inventory Management System.

---

## Sample Data

### Users

| name    | email              | role    | password     |
|---------|--------------------|---------|--------------|
| Admin   | admin@demo.com     | admin   | demo1234     |
| Manager | manager@demo.com   | manager | demo1234     |
| Worker  | worker@demo.com    | user    | demo1234     |

### InventoryItems

| name        | sku      | barcode   | expected_quantity | actual_quantity | category   | location   |
|-------------|----------|-----------|-------------------|----------------|------------|------------|
| Widget A    | WIDGET-A | 123456789 | 100               | 98             | Widgets    | Shelf 1    |
| Gadget B    | GADG-B   | 987654321 | 50                | 50             | Gadgets    | Shelf 2    |
| Screw Pack  | SCR-001  | 112233445 | 200               | 190            | Fasteners  | Bin 3      |

### AuditSessions

| session_id | user_id | start_time           | end_time             | status    | items_scanned | discrepancies_found | notes            |
|------------|---------|----------------------|----------------------|-----------|---------------|--------------------|------------------|
| uuid1      | 1       | 2025-09-29 12:00:00  | 2025-09-29 13:00:00  | completed | 3             | 2                  | Monthly audit    |
| uuid2      | 2       | 2025-09-29 14:00:00  |                      | active    | 1             | 0                  | In progress      |

### AuditLogs

| session_id | user_id | item_id | action | old_quantity | new_quantity | discrepancy | timestamp           | notes         |
|------------|---------|---------|--------|--------------|--------------|-------------|---------------------|---------------|
| 1          | 1       | 1       | scan   | 100          | 98           | -2          | 2025-09-29 12:10:00 | Found 2 less  |
| 1          | 1       | 2       | scan   | 50           | 50           | 0           | 2025-09-29 12:20:00 |               |

### Settings

| user_id | theme | icon_set    |
|---------|-------|-------------|
| 1       | dark  | fontawesome |
| 2       | light | bootstrap   |
| 3       | blue  | fontawesome |

---

## Workflows

### 1. Inventory Audit Workflow

1. Manager starts a new audit session.
2. Worker scans inventory items using barcode/SKU.
3. System records actual quantities, compares with expected, and logs discrepancies.
4. Session is paused or completed by Manager/Admin.
5. Audit report is generated/exported.

### 2. Inventory CRUD Workflow

1. Admin adds new items via web interface or CSV import.
2. Manager updates item quantities after receiving stock.
3. User searches and filters inventory items for details.
4. Admin deletes obsolete items (with audit logging).

### 3. User Preferences Workflow

1. Any user sets theme and icon preferences in Settings.
2. Preferences are saved and applied on next login.

### 4. Notifications Workflow

1. Real-time notifications sent to users when audits are started, completed, or discrepancies found.
2. Users see live progress and alerts on dashboard.

---

*Update this section with more sample data and workflow scenarios as your requirements expand!*