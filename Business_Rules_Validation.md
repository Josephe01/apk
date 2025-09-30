# Business Rules & Validation Details

This section specifies all critical business rules, validation logic, and constraints for the Inventory Management System.  
AI should use these rules for migrations, form requests, controllers, API, and frontend validation.

---

## Users

- **name:** required, max 100 characters
- **email:** required, must be valid email format, unique
- **password:** required, min 8 characters, must be hashed
- **role:** required, one of: admin, manager, user

---

## InventoryItems

- **name:** required, max 100 characters
- **sku:** required, unique, max 50 characters, only alphanumeric and dashes allowed
- **barcode:** optional, unique if present, max 100 characters
- **expected_quantity:** required, integer, >= 0
- **actual_quantity:** required, integer, >= 0
- **category:** required, max 50 characters
- **location:** optional, max 100 characters

---

## AuditSessions

- **session_id:** required, UUID, unique
- **user_id:** required, must exist in users table
- **start_time:** required, valid timestamp, must be before end_time
- **end_time:** optional, valid timestamp, must be after start_time
- **status:** required, one of: active, completed, cancelled
- **items_scanned:** integer, >= 0
- **discrepancies_found:** integer, >= 0
- **notes:** optional, max 1000 characters
- **Completion Rule:** Audit session cannot be marked as 'completed' until all inventory items have been scanned.

---

## AuditLogs

- **session_id:** required, must exist in audit_sessions table
- **user_id:** required, must exist in users table
- **item_id:** required, must exist in inventory_items table
- **action:** required, one of: scan, adjust, note
- **old_quantity:** optional, integer, >= 0
- **new_quantity:** optional, integer, >= 0
- **discrepancy:** required, integer, can be negative or positive, reflects (new_quantity - expected_quantity)
- **timestamp:** required, valid timestamp
- **notes:** optional, max 1000 characters

---

## Settings

- **user_id:** required, must exist in users table, one settings row per user
- **theme:** required, one of: light, dark, blue
- **icon_set:** required, one of: fontawesome, bootstrap

---

## General Business Rules

- **Unique Constraints:** email, sku, barcode (if present), session_id (audit_sessions)
- **Referential Integrity:** All foreign keys must reference valid, existing rows.
- **Input Sanitization:** All text fields must be sanitized to prevent XSS.
- **Role-based Access:** Only admins can delete users; only managers/admins can start/complete audits; users can only view their own settings.
- **Audit Logging:** All changes to inventory or audits must be logged in AuditLogs.
- **Bulk Actions:** Bulk import/export must validate all rows and return errors for invalid data.

---

*Update this file as new business rules or validation requirements are added!*