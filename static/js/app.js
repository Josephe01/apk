/**
 * Inventory Management System - Client-side JavaScript
 * Handles WebSocket connections, real-time updates, and UI interactions
 */

class InventoryApp {
    constructor() {
        this.socket = null;
        this.currentUser = null;
        this.activeSession = null;
        this.init();
    }

    init() {
        this.initWebSocket();
        this.setupEventListeners();
        this.checkActiveSession();
        this.loadUserPreferences();
    }

    initWebSocket() {
        // Initialize Socket.IO connection
        this.socket = io();
        
        // Connection events
        this.socket.on('connect', () => {
            console.log('Connected to server');
            this.socket.emit('join_room', 'all_users');
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
        });

        // Audit session events
        this.socket.on('audit_started', (data) => {
            this.showAuditBanner(data);
            this.showNotification(`${data.user} started an inventory check`, 'info');
        });

        this.socket.on('audit_updated', (data) => {
            this.updateAuditBanner(data);
        });

        this.socket.on('audit_completed', (data) => {
            this.hideAuditBanner();
            this.showNotification(`Inventory check completed by ${data.user}`, 'success');
        });

        this.socket.on('item_scanned', (data) => {
            this.handleItemScanned(data);
        });

        this.socket.on('discrepancy_found', (data) => {
            this.showNotification(`Discrepancy found: ${data.item_name} (${data.discrepancy})`, 'warning');
        });

        // Theme update events
        this.socket.on('theme_updated', (data) => {
            if (data.user_id === this.currentUser.id || data.is_global) {
                this.applyTheme(data.theme_config);
                this.showNotification('Theme updated', 'info');
            }
        });

        this.socket.on('preferences_updated', (data) => {
            this.applyUserPreferences(data);
        });
    }

    setupEventListeners() {
        // Page visibility change - reconnect if needed
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && !this.socket.connected) {
                this.socket.connect();
            }
        });

        // Handle page refresh/close
        window.addEventListener('beforeunload', () => {
            if (this.socket) {
                this.socket.disconnect();
            }
        });
    }

    checkActiveSession() {
        // Check if there's an active audit session
        fetch('/api/active_session')
            .then(response => response.json())
            .then(data => {
                if (data.session) {
                    this.showAuditBanner(data.session);
                }
            })
            .catch(error => console.error('Error checking active session:', error));
    }

    showAuditBanner(sessionData) {
        const banner = document.getElementById('audit-banner');
        if (!banner) return;

        // Update banner content
        document.getElementById('audit-user').textContent = sessionData.user;
        document.getElementById('audit-start-time').textContent = this.formatDateTime(sessionData.start_time);
        document.getElementById('audit-items-count').textContent = sessionData.items_scanned || 0;
        document.getElementById('audit-discrepancies').textContent = sessionData.discrepancies_found || 0;

        // Show banner with animation
        banner.classList.remove('d-none');
        banner.classList.add('active');
        
        this.activeSession = sessionData;
    }

    updateAuditBanner(sessionData) {
        if (!this.activeSession) return;

        // Update counters
        document.getElementById('audit-items-count').textContent = sessionData.items_scanned || 0;
        document.getElementById('audit-discrepancies').textContent = sessionData.discrepancies_found || 0;

        // Add pulse animation to updated elements
        const itemsCount = document.getElementById('audit-items-count');
        const discrepancies = document.getElementById('audit-discrepancies');
        
        itemsCount.classList.add('pulse');
        discrepancies.classList.add('pulse');
        
        setTimeout(() => {
            itemsCount.classList.remove('pulse');
            discrepancies.classList.remove('pulse');
        }, 2000);
    }

    hideAuditBanner() {
        const banner = document.getElementById('audit-banner');
        if (banner) {
            banner.classList.add('d-none');
            banner.classList.remove('active');
        }
        this.activeSession = null;
    }

    handleItemScanned(data) {
        // Update inventory table if visible
        const table = document.getElementById('inventoryTable');
        if (table) {
            this.updateInventoryRow(data.item_id, data);
        }

        // Show scan notification
        this.showNotification(`Item scanned: ${data.item_name}`, 'info');
    }

    updateInventoryRow(itemId, data) {
        const rows = document.querySelectorAll('#inventoryTable tbody tr');
        rows.forEach(row => {
            const firstCell = row.cells[0];
            if (firstCell && firstCell.dataset.itemId == itemId) {
                // Update actual quantity
                const actualCell = row.cells[6];
                if (actualCell) {
                    actualCell.innerHTML = `<span class="badge bg-info">${data.actual_quantity}</span>`;
                }

                // Update discrepancy
                const discrepancyCell = row.cells[7];
                if (discrepancyCell) {
                    const diff = data.actual_quantity - data.expected_quantity;
                    let badgeClass = 'bg-success';
                    let icon = '<i class="fas fa-check me-1"></i>';
                    
                    if (diff > 0) {
                        badgeClass = 'bg-warning';
                        icon = '<i class="fas fa-arrow-up me-1"></i>';
                    } else if (diff < 0) {
                        badgeClass = 'bg-danger';
                        icon = '<i class="fas fa-arrow-down me-1"></i>';
                    }
                    
                    discrepancyCell.innerHTML = `<span class="badge ${badgeClass}">${icon}${diff}</span>`;
                }

                // Add highlight animation
                row.classList.add('table-warning');
                setTimeout(() => {
                    row.classList.remove('table-warning');
                }, 3000);
            }
        });
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    formatDateTime(isoString) {
        const date = new Date(isoString);
        return date.toLocaleString();
    }

    // API Helper Methods
    async apiCall(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const response = await fetch(url, { ...defaultOptions, ...options });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return response.json();
    }

    // Audit Session Methods
    async startAuditSession() {
        try {
            const data = await this.apiCall('/start_audit', { method: 'POST' });
            if (data.success) {
                this.showNotification('Audit session started successfully!', 'success');
                return data.session_id;
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            this.showNotification(`Error: ${error.message}`, 'danger');
            throw error;
        }
    }

    async endAuditSession(sessionId) {
        try {
            const data = await this.apiCall(`/api/session/${sessionId}/end`, { method: 'POST' });
            if (data.success) {
                this.showNotification('Audit session completed!', 'success');
                return data;
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            this.showNotification(`Error: ${error.message}`, 'danger');
            throw error;
        }
    }

    async scanItem(sessionId, barcode, actualQuantity) {
        try {
            const data = await this.apiCall('/api/scan', {
                method: 'POST',
                body: JSON.stringify({
                    session_id: sessionId,
                    barcode: barcode,
                    actual_quantity: actualQuantity
                })
            });
            
            if (data.success) {
                return data;
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            this.showNotification(`Scan error: ${error.message}`, 'danger');
            throw error;
        }
    }

    // Theme Management Methods
    async loadUserPreferences() {
        try {
            const data = await this.apiCall('/api/user/preferences');
            this.applyUserPreferences(data);
            return data;
        } catch (error) {
            console.error('Failed to load user preferences:', error);
            return null;
        }
    }

    applyUserPreferences(preferences) {
        // Apply font size
        const fontSizeMap = {
            'small': '14px',
            'medium': '16px', 
            'large': '18px',
            'x-large': '20px'
        };
        
        if (preferences.font_size) {
            document.body.style.fontSize = fontSizeMap[preferences.font_size] || '16px';
        }

        // Apply high contrast
        if (preferences.high_contrast) {
            document.body.classList.add('high-contrast');
        } else {
            document.body.classList.remove('high-contrast');
        }

        // Apply dark mode
        if (preferences.dark_mode) {
            document.body.setAttribute('data-bs-theme', 'dark');
        } else {
            document.body.removeAttribute('data-bs-theme');
        }

        // Apply theme if specified
        if (preferences.theme_id) {
            this.loadAndApplyTheme(preferences.theme_id);
        }
    }

    async loadAndApplyTheme(themeId) {
        try {
            const themes = await this.apiCall('/api/themes');
            const theme = themes.find(t => t.id == themeId);
            if (theme && theme.config) {
                this.applyTheme(theme.config);
            }
        } catch (error) {
            console.error('Failed to load theme:', error);
        }
    }

    applyTheme(config) {
        if (!config) return;

        const root = document.documentElement;
        
        // Apply CSS custom properties for Bootstrap variables
        if (config.primaryColor) root.style.setProperty('--bs-primary', config.primaryColor);
        if (config.secondaryColor) root.style.setProperty('--bs-secondary', config.secondaryColor);
        if (config.successColor) root.style.setProperty('--bs-success', config.successColor);
        if (config.dangerColor) root.style.setProperty('--bs-danger', config.dangerColor);
        if (config.warningColor) root.style.setProperty('--bs-warning', config.warningColor);
        if (config.infoColor) root.style.setProperty('--bs-info', config.infoColor);
        if (config.backgroundColor) root.style.setProperty('--bs-body-bg', config.backgroundColor);
        if (config.textColor) root.style.setProperty('--bs-body-color', config.textColor);

        // Apply typography
        if (config.fontFamily) {
            document.body.style.fontFamily = config.fontFamily;
        }
        if (config.baseFontSize) {
            document.body.style.fontSize = config.baseFontSize;
        }

        // Store current theme config for persistence
        this.currentThemeConfig = config;
    }

    async toggleDarkMode() {
        const preferences = await this.loadUserPreferences();
        if (preferences) {
            const newDarkMode = !preferences.dark_mode;
            this.updateUserPreferences({ dark_mode: newDarkMode });
        }
    }

    async updateUserPreferences(updates) {
        try {
            const data = await this.apiCall('/api/user/preferences', {
                method: 'PUT',
                body: JSON.stringify(updates)
            });
            
            if (data.success) {
                this.showNotification('Preferences updated', 'success');
                return data;
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            this.showNotification(`Failed to update preferences: ${error.message}`, 'danger');
            throw error;
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.inventoryApp = new InventoryApp();
});

// Global utility functions
function startAudit() {
    if (window.inventoryApp) {
        window.inventoryApp.startAuditSession()
            .then(sessionId => {
                if (sessionId) {
                    window.location.href = `/audit/${sessionId}`;
                }
            })
            .catch(error => {
                console.error('Failed to start audit:', error);
            });
    }
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat().format(number);
}

function downloadReport(sessionId, format = 'pdf') {
    const url = `/api/session/${sessionId}/export?format=${format}`;
    const link = document.createElement('a');
    link.href = url;
    link.download = `audit_report_${sessionId}.${format}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}