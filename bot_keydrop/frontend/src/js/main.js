/**
 * Main application entry point
 * Initializes and coordinates all components
 */

class KeydropBotApp {
    constructor() {
        this.isInitialized = false;
        this.connectionStatus = 'disconnected';
        this.retryCount = 0;
        this.maxRetries = 5;
    }

    /**
     * Initialize the application
     */
    async init() {
        if (this.isInitialized) return;

        try {
            console.log('Initializing Keydrop Bot Professional...');
            
            // Show loading state
            this.showLoadingState();

            // Check backend connection
            await this.checkBackendConnection();

            // Initialize UI Manager
            await window.uiManager.init();

            // Setup global error handling
            this.setupErrorHandling();

            // Setup connection monitoring
            this.setupConnectionMonitoring();

            // Hide loading state
            this.hideLoadingState();

            this.isInitialized = true;
            console.log('Keydrop Bot Professional initialized successfully');

        } catch (error) {
            console.error('Failed to initialize application:', error);
            this.showErrorState(error.message);
        }
    }

    /**
     * Check if backend is available
     */
    async checkBackendConnection() {
        try {
            const isHealthy = await window.apiClient.healthCheck();
            if (!isHealthy) {
                throw new Error('Backend health check failed');
            }
            this.connectionStatus = 'connected';
            this.retryCount = 0;
        } catch (error) {
            this.connectionStatus = 'disconnected';
            throw new Error('Não foi possível conectar ao backend. Verifique se o servidor está executando.');
        }
    }

    /**
     * Setup global error handling
     */
    setupErrorHandling() {
        // Handle unhandled promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
            window.uiManager.showNotification('Erro inesperado na aplicação', 'error');
            event.preventDefault();
        });

        // Handle uncaught errors
        window.addEventListener('error', (event) => {
            console.error('Uncaught error:', event.error);
            window.uiManager.showNotification('Erro inesperado na aplicação', 'error');
        });
    }

    /**
     * Setup connection monitoring
     */
    setupConnectionMonitoring() {
        // Monitor WebSocket connection
        window.apiClient.on('websocket:connected', () => {
            this.connectionStatus = 'connected';
            this.retryCount = 0;
            this.updateConnectionStatus();
        });

        window.apiClient.on('websocket:disconnected', () => {
            this.connectionStatus = 'disconnected';
            this.updateConnectionStatus();
        });

        window.apiClient.on('websocket:error', () => {
            this.connectionStatus = 'error';
            this.updateConnectionStatus();
        });

        // Periodic health check
        setInterval(async () => {
            if (this.connectionStatus === 'disconnected' && this.retryCount < this.maxRetries) {
                try {
                    await this.checkBackendConnection();
                    this.updateConnectionStatus();
                } catch (error) {
                    this.retryCount++;
                    if (this.retryCount >= this.maxRetries) {
                        window.uiManager.showNotification(
                            'Conexão com o backend perdida. Verifique o servidor.', 
                            'error'
                        );
                    }
                }
            }
        }, 10000); // Check every 10 seconds
    }

    /**
     * Update connection status in UI
     */
    updateConnectionStatus() {
        const statusElement = document.getElementById('connectionStatus');
        if (statusElement) {
            statusElement.className = `connection-status ${this.connectionStatus}`;
            statusElement.textContent = this.getConnectionStatusText();
        }
    }

    /**
     * Get connection status text
     */
    getConnectionStatusText() {
        switch (this.connectionStatus) {
            case 'connected':
                return 'Conectado';
            case 'disconnected':
                return 'Desconectado';
            case 'error':
                return 'Erro de Conexão';
            default:
                return 'Desconhecido';
        }
    }

    /**
     * Show loading state
     */
    showLoadingState() {
        const loadingOverlay = document.createElement('div');
        loadingOverlay.id = 'loadingOverlay';
        loadingOverlay.className = 'loading-overlay';
        loadingOverlay.innerHTML = `
            <div class="loading-content">
                <div class="loading-spinner"></div>
                <h2>Carregando Keydrop Bot Professional</h2>
                <p>Conectando ao servidor...</p>
            </div>
        `;
        document.body.appendChild(loadingOverlay);
    }

    /**
     * Hide loading state
     */
    hideLoadingState() {
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) {
            loadingOverlay.remove();
        }
    }

    /**
     * Show error state
     */
    showErrorState(message) {
        this.hideLoadingState();
        
        const errorOverlay = document.createElement('div');
        errorOverlay.id = 'errorOverlay';
        errorOverlay.className = 'error-overlay';
        errorOverlay.innerHTML = `
            <div class="error-content">
                <div class="error-icon">❌</div>
                <h2>Erro ao Inicializar</h2>
                <p>${message}</p>
                <button class="retry-btn" onclick="window.location.reload()">
                    Tentar Novamente
                </button>
            </div>
        `;
        document.body.appendChild(errorOverlay);
    }

    /**
     * Handle application shutdown
     */
    shutdown() {
        if (!this.isInitialized) return;

        console.log('Shutting down Keydrop Bot Professional...');

        // Cleanup UI Manager
        if (window.uiManager) {
            window.uiManager.destroy();
        }

        // Disconnect API client
        if (window.apiClient) {
            window.apiClient.disconnect();
        }

        this.isInitialized = false;
    }
}

/**
 * Utility functions
 */
const Utils = {
    /**
     * Format date for display
     */
    formatDate(date) {
        return new Intl.DateTimeFormat('pt-BR', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        }).format(new Date(date));
    },

    /**
     * Format number for display
     */
    formatNumber(number) {
        return new Intl.NumberFormat('pt-BR').format(number);
    },

    /**
     * Format bytes for display
     */
    formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';

        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];

        const i = Math.floor(Math.log(bytes) / Math.log(k));

        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    },

    /**
     * Debounce function
     */
    debounce(func, wait, immediate = false) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                timeout = null;
                if (!immediate) func(...args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func(...args);
        };
    },

    /**
     * Throttle function
     */
    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    /**
     * Validate configuration
     */
    validateConfig(config) {
        const errors = [];

        if (!config.numTabs || config.numTabs < 1 || config.numTabs > 100) {
            errors.push('Número de guias deve estar entre 1 e 100');
        }

        if (!config.executionSpeed || config.executionSpeed < 0.1 || config.executionSpeed > 10) {
            errors.push('Velocidade de execução deve estar entre 0.1x e 10x');
        }

        if (!config.retryAttempts || config.retryAttempts < 1 || config.retryAttempts > 20) {
            errors.push('Tentativas de retry devem estar entre 1 e 20');
        }

        if (config.discordWebhook && !config.discordWebhook.startsWith('https://discord.com/api/webhooks/')) {
            errors.push('URL do webhook Discord inválida');
        }

        return errors;
    },

    /**
     * Generate unique ID
     */
    generateId() {
        return Math.random().toString(36).substr(2, 9);
    },

    /**
     * Copy text to clipboard
     */
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (error) {
            console.error('Failed to copy to clipboard:', error);
            return false;
        }
    },

    /**
     * Download data as file
     */
    downloadData(data, filename, type = 'application/json') {
        const blob = new Blob([data], { type });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
};

// Global app instance
window.keydropApp = new KeydropBotApp();
window.Utils = Utils;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    try {
        await window.keydropApp.init();
    } catch (error) {
        console.error('Failed to start application:', error);
    }
});

// Handle page unload
window.addEventListener('beforeunload', () => {
    window.keydropApp.shutdown();
});
