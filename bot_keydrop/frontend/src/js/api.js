/**
 * API Client for Keydrop Bot Professional
 * Handles all communication with the backend FastAPI server
 */

class ApiClient {
    constructor() {
        this.baseUrl = 'http://localhost:8000';
        this.wsUrl = 'ws://localhost:8000/ws';
        this.websocket = null;
        this.eventListeners = new Map();
    }

    /**
     * Generic HTTP request method
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        try {
            const response = await fetch(url, { ...defaultOptions, ...options });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }
            
            return await response.text();
        } catch (error) {
            console.error(`API request failed: ${endpoint}`, error);
            throw error;
        }
    }

    /**
     * Configuration Management
     */
    async getConfig() {
        return await this.request('/config');
    }

    async updateConfig(config) {
        return await this.request('/config', {
            method: 'PUT',
            body: JSON.stringify(config)
        });
    }

    async resetConfig() {
        return await this.request('/config/reset', {
            method: 'POST'
        });
    }

    /**
     * Bot Control
     */
    async startBot() {
        return await this.request('/bot/control', {
            method: 'POST',
            body: JSON.stringify({ action: 'start' })
        });
    }

    async stopBot() {
        return await this.request('/bot/control', {
            method: 'POST',
            body: JSON.stringify({ action: 'stop' })
        });
    }

    async emergencyStop() {
        return await this.request('/bot/control', {
            method: 'POST',
            body: JSON.stringify({ action: 'emergency_stop' })
        });
    }

    async getStatus() {
        return await this.request('/bot/status');
    }

    /**
     * Statistics
     */
    async getStats() {
        return await this.request('/stats/participation');
    }

    async getDetailedStats() {
        return await this.request('/stats/participation/history');
    }

    async resetStats() {
        return await this.request('/stats/reset', {
            method: 'POST'
        });
    }

    /**
     * Reports
     */
    async getReports(startDate = null, endDate = null) {
        let endpoint = '/reports';
        const params = new URLSearchParams();
        
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        
        if (params.toString()) {
            endpoint += `?${params.toString()}`;
        }
        
        return await this.request(endpoint);
    }

    async exportReport(format = 'json') {
        return await this.request(`/reports/export?format=${format}`);
    }

    /**
     * System Monitoring
     */
    async getSystemInfo() {
        return await this.request('/stats/system');
    }

    async getBrowserInstances() {
        return await this.request('/bot/tabs');
    }

    async teachAI() {
        return await this.request('/learning/teach', { method: 'POST' });
    }

    async testKeydrop() {
        return await this.request('/diagnostics/keydrop');
    }

    async testLogin() {
        return await this.request('/diagnostics/login');
    }

    async testNotification() {
        return await this.request('/diagnostics/notification', { method: 'POST' });
    }

    async testProxy(proxy) {
        return await this.request('/diagnostics/proxy', {
            method: 'POST',
            body: JSON.stringify({ proxy })
        });
    }

    /**
     * WebSocket Connection Management
     */
    connectWebSocket() {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            return;
        }

        try {
            this.websocket = new WebSocket(this.wsUrl);
            
            this.websocket.onopen = () => {
                console.log('WebSocket connected');
                this.emit('websocket:connected');
            };

            this.websocket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleWebSocketMessage(data);
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error);
                }
            };

            this.websocket.onclose = (event) => {
                console.log('WebSocket disconnected:', event.code, event.reason);
                this.emit('websocket:disconnected');
                
                // Reconnect after 3 seconds
                setTimeout(() => {
                    this.connectWebSocket();
                }, 3000);
            };

            this.websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.emit('websocket:error', error);
            };

        } catch (error) {
            console.error('Error creating WebSocket connection:', error);
        }
    }

    /**
     * Handle incoming WebSocket messages
     */
    handleWebSocketMessage(data) {
        const { type, data: payload } = data;
        
        switch (type) {
            case 'bot_status':
                this.emit('bot:status', payload);
                break;
            case 'stats_update':
                this.emit('stats:update', payload);
                break;
            case 'system_metrics':
                this.emit('system:info', payload);
                break;
            case 'browser_status':
                this.emit('browser:status', payload);
                break;
            case 'task_completed':
                this.emit('task:completed', payload);
                break;
            case 'error':
                this.emit('error', payload);
                break;
            case 'notification':
                this.emit('notification', payload);
                break;
            default:
                console.warn('Unknown WebSocket message type:', type);
        }
    }

    /**
     * Send message through WebSocket
     */
    sendWebSocketMessage(type, payload = {}) {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.send(JSON.stringify({ type, data: payload }));
        } else {
            console.warn('WebSocket not connected');
        }
    }

    /**
     * Event system for handling real-time updates
     */
    on(event, callback) {
        if (!this.eventListeners.has(event)) {
            this.eventListeners.set(event, []);
        }
        this.eventListeners.get(event).push(callback);
    }

    off(event, callback) {
        if (this.eventListeners.has(event)) {
            const listeners = this.eventListeners.get(event);
            const index = listeners.indexOf(callback);
            if (index > -1) {
                listeners.splice(index, 1);
            }
        }
    }

    emit(event, data) {
        if (this.eventListeners.has(event)) {
            this.eventListeners.get(event).forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Error in event listener for ${event}:`, error);
                }
            });
        }
    }

    /**
     * Disconnect WebSocket
     */
    disconnect() {
        if (this.websocket) {
            this.websocket.close();
            this.websocket = null;
        }
    }

    /**
     * Health check
     */
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseUrl}/health`);
            return response.ok;
        } catch (error) {
            console.error('Health check failed:', error);
            return false;
        }
    }
}

// Export singleton instance
window.apiClient = new ApiClient();
