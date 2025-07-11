/**
 * UI Manager for Keydrop Bot Professional
 * Handles all user interface interactions and updates
 */

class UIManager {
    constructor() {
        this.currentTab = 'config';
        this.isInitialized = false;
        this.config = {};
        this.stats = {};
        this.systemInfo = {};
        this.updateIntervals = new Map();
        
        // Sound notification system
        this.soundEnabled = localStorage.getItem('soundNotifications') !== 'false';
        this.audioContext = null;
        this.sounds = {
            success: { frequency: 800, duration: 200 },
            error: { frequency: 400, duration: 500 },
            warning: { frequency: 600, duration: 300 },
            emergency: { frequency: 300, duration: 1000 }
        };
        
        // Bind methods
        this.handleTabSwitch = this.handleTabSwitch.bind(this);
        this.handleConfigChange = this.handleConfigChange.bind(this);
        this.handleEmergencyStop = this.handleEmergencyStop.bind(this);
    }

    /**
     * Initialize the UI Manager
     */
    async init() {
        if (this.isInitialized) return;

        try {
            await this.setupEventListeners();
            await this.loadInitialData();
            await this.setupRealTimeUpdates();
            this.isInitialized = true;
            console.log('UI Manager initialized successfully');
        } catch (error) {
            console.error('Failed to initialize UI Manager:', error);
            this.showNotification('Erro ao inicializar interface', 'error');
        }
    }

    /**
     * Setup event listeners for UI elements
     */
    async setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.tab-button').forEach(button => {
            button.addEventListener('click', this.handleTabSwitch);
        });

        // Emergency stop button
        const emergencyBtn = document.getElementById('emergencyStopBtn');
        if (emergencyBtn) {
            emergencyBtn.addEventListener('click', this.handleEmergencyStop);
        }

        // Configuration form elements
        this.setupConfigEventListeners();

        // Control buttons
        this.setupControlEventListeners();

        // Reports and exports
        this.setupReportsEventListeners();
    }

    /**
     * Setup configuration form event listeners
     */
    setupConfigEventListeners() {
        const configElements = [
            'numTabs', 'executionSpeed', 'retryAttempts',
            'headlessMode', 'miniWindowMode', 'enableStealth',
            'keepCookies', 'discordWebhook', 'discordNotifications',
            'systemMonitoring', 'enableLogging', 'autoRestart'
        ];

        configElements.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                const eventType = element.type === 'checkbox' ? 'change' : 
                                element.type === 'range' ? 'input' : 'change';
                element.addEventListener(eventType, this.handleConfigChange);
            }
        });

        // Special handling for speed slider
        const speedSlider = document.getElementById('executionSpeed');
        if (speedSlider) {
            speedSlider.addEventListener('input', (e) => {
                const speedValue = document.getElementById('speedValue');
                if (speedValue) {
                    speedValue.textContent = `${parseFloat(e.target.value).toFixed(1)}x`;
                }
            });
        }
    }

    /**
     * Setup control button event listeners
     */
    setupControlEventListeners() {
        const startBtn = document.getElementById('startBtn');
        const stopBtn = document.getElementById('stopBtn');
        const clearCacheBtn = document.getElementById('clearCacheBtn');
        const checkUpdateBtn = document.getElementById('checkUpdateBtn');
        const saveConfigBtn = document.getElementById('saveConfigBtn');
        const resetConfigBtn = document.getElementById('resetConfigBtn');

        if (startBtn) {
            startBtn.addEventListener('click', async () => {
                await this.startBot();
            });
        }

        if (stopBtn) {
            stopBtn.addEventListener('click', async () => {
                await this.stopBot();
            });
        }

        if (clearCacheBtn) {
            clearCacheBtn.addEventListener('click', async () => {
                await this.clearCache();
            });
        }

        if (checkUpdateBtn) {
            checkUpdateBtn.addEventListener('click', async () => {
                await this.checkForUpdates();
            });
        }

        if (saveConfigBtn) {
            saveConfigBtn.addEventListener('click', async () => {
                await this.saveConfig();
            });
        }

        if (resetConfigBtn) {
            resetConfigBtn.addEventListener('click', async () => {
                await this.resetConfig();
            });
        }
    }

    /**
     * Setup reports and export event listeners
     */
    setupReportsEventListeners() {
        const exportJsonBtn = document.getElementById('exportJsonBtn');
        const exportCsvBtn = document.getElementById('exportCsvBtn');
        const refreshReportsBtn = document.getElementById('refreshReportsBtn');

        if (exportJsonBtn) {
            exportJsonBtn.addEventListener('click', () => this.exportReport('json'));
        }

        if (exportCsvBtn) {
            exportCsvBtn.addEventListener('click', () => this.exportReport('csv'));
        }

        if (refreshReportsBtn) {
            refreshReportsBtn.addEventListener('click', () => this.refreshReports());
        }
    }

    /**
     * Load initial data from the backend
     */
    async loadInitialData() {
        try {
            // Load configuration
            this.config = await window.apiClient.getConfig();
            this.updateConfigUI();

            // Load current status
            const status = await window.apiClient.getStatus();
            this.updateBotStatus(status);

            // Load statistics
            this.stats = await window.apiClient.getStats();
            this.updateStatsUI();

            // Load system information
            this.systemInfo = await window.apiClient.getSystemInfo();
            this.updateSystemInfoUI();

        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showNotification('Erro ao carregar dados iniciais', 'error');
        }
    }

    /**
     * Setup real-time updates via WebSocket
     */
    async setupRealTimeUpdates() {
        // Connect to WebSocket
        window.apiClient.connectWebSocket();

        // Setup event listeners for real-time updates
        window.apiClient.on('bot:status', (status) => {
            this.updateBotStatus(status);
        });

        window.apiClient.on('stats:update', (stats) => {
            this.stats = { ...this.stats, ...stats };
            this.updateStatsUI();
        });

        window.apiClient.on('system:info', (systemInfo) => {
            this.systemInfo = { ...this.systemInfo, ...systemInfo };
            this.updateSystemInfoUI();
        });

        window.apiClient.on('notification', (notification) => {
            this.showNotification(notification.message, notification.type);
        });

        window.apiClient.on('error', (error) => {
            this.showNotification(error.message, 'error');
        });

        // Setup periodic updates for non-realtime data
        this.updateIntervals.set('reports', setInterval(() => {
            if (this.currentTab === 'reports') {
                this.refreshReports();
            }
        }, 30000)); // Update reports every 30 seconds
    }

    /**
     * Handle tab switching
     */
    handleTabSwitch(event) {
        const tabName = event.currentTarget.dataset.tab;
        if (!tabName || tabName === this.currentTab) return;

        // Update tab buttons
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.classList.remove('active');
        });
        event.currentTarget.classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        
        const targetContent = document.getElementById(tabName);
        if (targetContent) {
            targetContent.classList.add('active');
        }

        this.currentTab = tabName;

        // Load tab-specific data
        this.loadTabData(tabName);
    }

    /**
     * Load data specific to the current tab
     */
    async loadTabData(tabName) {
        try {
            switch (tabName) {
                case 'stats':
                    this.stats = await window.apiClient.getDetailedStats();
                    this.updateStatsUI();
                    break;
                case 'reports':
                    await this.refreshReports();
                    break;
            }
        } catch (error) {
            console.error(`Error loading data for tab ${tabName}:`, error);
        }
    }

    /**
     * Handle configuration changes
     */
    handleConfigChange(event) {
        const { id, type, value, checked } = event.target;
        
        if (type === 'checkbox') {
            this.config[id] = checked;
        } else if (type === 'number' || type === 'range') {
            this.config[id] = parseFloat(value);
        } else {
            this.config[id] = value;
        }

        // Mark config as modified
        this.markConfigModified();
    }

    /**
     * Mark configuration as modified
     */
    markConfigModified() {
        const saveBtn = document.getElementById('saveConfigBtn');
        if (saveBtn) {
            saveBtn.classList.add('modified');
            saveBtn.textContent = 'Salvar Alterações';
        }
    }

    /**
     * Handle emergency stop
     */
    async handleEmergencyStop() {
        try {
            await window.apiClient.emergencyStop();
            this.showNotification('Parada de emergência ativada!', 'warning');
            this.playSound('emergency');
        } catch (error) {
            console.error('Emergency stop failed:', error);
            this.showNotification('Erro na parada de emergência', 'error');
        }
    }

    /**
     * Start the bot
     */
    async startBot() {
        try {
            const startBtn = document.getElementById('startBtn');
            if (startBtn) {
                startBtn.disabled = true;
                startBtn.textContent = 'Iniciando...';
            }

            await window.apiClient.startBot();
            this.showNotification('Bot iniciado com sucesso!', 'success');
            this.playSound('success');

        } catch (error) {
            console.error('Failed to start bot:', error);
            this.showNotification('Erro ao iniciar o bot', 'error');
        } finally {
            const startBtn = document.getElementById('startBtn');
            if (startBtn) {
                startBtn.disabled = false;
                startBtn.textContent = 'Iniciar Bot';
            }
        }
    }

    /**
     * Stop the bot
     */
    async stopBot() {
        try {
            const stopBtn = document.getElementById('stopBtn');
            if (stopBtn) {
                stopBtn.disabled = true;
                stopBtn.textContent = 'Parando...';
            }

            await window.apiClient.stopBot();
            this.showNotification('Bot parado com sucesso!', 'success');
            this.playSound('success');

        } catch (error) {
            console.error('Failed to stop bot:', error);
            this.showNotification('Erro ao parar o bot', 'error');
        } finally {
            const stopBtn = document.getElementById('stopBtn');
            if (stopBtn) {
                stopBtn.disabled = false;
                stopBtn.textContent = 'Parar Bot';
            }
        }
    }

    /**
     * Save configuration
     */
    async saveConfig() {
        try {
            const saveBtn = document.getElementById('saveConfigBtn');
            if (saveBtn) {
                saveBtn.disabled = true;
                saveBtn.textContent = 'Salvando...';
            }

            await window.apiClient.updateConfig(this.config);
            this.showNotification('Configuração salva com sucesso!', 'success');

            if (saveBtn) {
                saveBtn.classList.remove('modified');
                saveBtn.textContent = 'Configuração Salva';
            }

        } catch (error) {
            console.error('Failed to save config:', error);
            this.showNotification('Erro ao salvar configuração', 'error');
        } finally {
            const saveBtn = document.getElementById('saveConfigBtn');
            if (saveBtn) {
                saveBtn.disabled = false;
                if (!saveBtn.classList.contains('modified')) {
                    saveBtn.textContent = 'Salvar Configuração';
                }
            }
        }
    }

    /**
     * Reset configuration
     */
    async resetConfig() {
        if (!confirm('Tem certeza que deseja resetar todas as configurações?')) {
            return;
        }

        try {
            this.config = await window.apiClient.resetConfig();
            this.updateConfigUI();
            this.showNotification('Configuração resetada com sucesso!', 'success');
        } catch (error) {
            console.error('Failed to reset config:', error);
            this.showNotification('Erro ao resetar configuração', 'error');
        }
    }

    /**
     * Clear cache while keeping login data
     */
    async clearCache() {
        if (!confirm('Tem certeza que deseja limpar o cache? Os logins serão mantidos.')) {
            return;
        }

        try {
            const clearBtn = document.getElementById('clearCacheBtn');
            if (clearBtn) {
                clearBtn.disabled = true;
                clearBtn.textContent = 'Limpando...';
            }

            const response = await window.apiClient.request('/cache/clear', {
                method: 'POST',
                body: JSON.stringify({ preserve_login: true })
            });

            if (response.success) {
                this.showNotification('Cache limpo com sucesso! Logins mantidos.', 'success');
            } else {
                this.showNotification('Erro ao limpar cache', 'error');
            }

        } catch (error) {
            console.error('Failed to clear cache:', error);
            this.showNotification('Erro ao limpar cache', 'error');
        } finally {
            const clearBtn = document.getElementById('clearCacheBtn');
            if (clearBtn) {
                clearBtn.disabled = false;
                clearBtn.textContent = 'Limpar Cache';
            }
        }
    }

    /**
     * Check for application updates
     */
    async checkForUpdates() {
        try {
            const updateBtn = document.getElementById('checkUpdateBtn');
            if (updateBtn) {
                updateBtn.disabled = true;
                updateBtn.textContent = 'Verificando...';
            }

            // Simular verificação de atualização
            // Em uma implementação real, isso verificaria um servidor de atualizações
            await new Promise(resolve => setTimeout(resolve, 2000));

            const currentVersion = 'v2.1.0';
            const isLatest = true; // Simular que está atualizado

            if (isLatest) {
                this.showNotification(`Você está usando a versão mais recente (${currentVersion})`, 'success');
            } else {
                this.showNotification('Nova versão disponível! Visite o GitHub para baixar.', 'info');
            }

        } catch (error) {
            console.error('Failed to check for updates:', error);
            this.showNotification('Erro ao verificar atualizações', 'error');
        } finally {
            const updateBtn = document.getElementById('checkUpdateBtn');
            if (updateBtn) {
                updateBtn.disabled = false;
                updateBtn.textContent = 'Verificar Atualizações';
            }
        }
    }

    /**
     * Update configuration UI elements
     */
    updateConfigUI() {
        Object.entries(this.config).forEach(([key, value]) => {
            const element = document.getElementById(key);
            if (!element) return;

            if (element.type === 'checkbox') {
                element.checked = value;
            } else {
                element.value = value;
            }

            // Update speed value display
            if (key === 'executionSpeed') {
                const speedValue = document.getElementById('speedValue');
                if (speedValue) {
                    speedValue.textContent = `${parseFloat(value).toFixed(1)}x`;
                }
            }
        });
    }

    /**
     * Update bot status display
     */
    updateBotStatus(status) {
        const statusIndicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');

        if (statusIndicator && statusText) {
            statusIndicator.className = `status-indicator ${status.status}`;
            statusText.textContent = status.status_text || status.status;
        }

        // Update control buttons
        const startBtn = document.getElementById('startBtn');
        const stopBtn = document.getElementById('stopBtn');

        if (startBtn && stopBtn) {
            const isRunning = status.status === 'running';
            startBtn.disabled = isRunning;
            stopBtn.disabled = !isRunning;
        }
    }

    /**
     * Update statistics UI
     */
    updateStatsUI() {
        const statElements = {
            'totalParticipations': 'totalParticipations',
            'successfulParticipations': 'successfulParticipations',
            'failedParticipations': 'failedParticipations',
            'averageTime': 'averageTime',
            'activeBrowsers': 'activeBrowsers',
            'uptime': 'uptime'
        };

        Object.entries(statElements).forEach(([statKey, elementId]) => {
            const element = document.getElementById(elementId);
            if (element && this.stats[statKey] !== undefined) {
                element.textContent = this.formatStatValue(statKey, this.stats[statKey]);
            }
        });

        // Update success rate
        const successRateElement = document.getElementById('successRate');
        if (successRateElement && this.stats.totalParticipations > 0) {
            const rate = (this.stats.successfulParticipations / this.stats.totalParticipations * 100).toFixed(1);
            successRateElement.textContent = `${rate}%`;
        }
    }

    /**
     * Update system information UI
     */
    updateSystemInfoUI() {
        const systemElements = {
            'cpuUsage': 'cpuUsage',
            'memoryUsage': 'memoryUsage',
            'diskUsage': 'diskUsage'
        };

        Object.entries(systemElements).forEach(([statKey, elementId]) => {
            const element = document.getElementById(elementId);
            if (element && this.systemInfo[statKey] !== undefined) {
                element.textContent = this.formatSystemValue(statKey, this.systemInfo[statKey]);
            }
        });
    }

    /**
     * Format statistics values for display
     */
    formatStatValue(key, value) {
        switch (key) {
            case 'averageTime':
                return `${value.toFixed(2)}s`;
            case 'uptime':
                return this.formatUptime(value);
            default:
                return value.toString();
        }
    }

    /**
     * Format system values for display
     */
    formatSystemValue(key, value) {
        switch (key) {
            case 'cpuUsage':
            case 'memoryUsage':
            case 'diskUsage':
                return `${value.toFixed(1)}%`;
            default:
                return value.toString();
        }
    }

    /**
     * Format uptime for display
     */
    formatUptime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    /**
     * Refresh reports data
     */
    async refreshReports() {
        try {
            const reports = await window.apiClient.getReports();
            this.updateReportsUI(reports);
        } catch (error) {
            console.error('Failed to refresh reports:', error);
            this.showNotification('Erro ao atualizar relatórios', 'error');
        }
    }

    /**
     * Update reports UI
     */
    updateReportsUI(reports) {
        // This would update the reports table/list
        // Implementation depends on the specific reports structure
        console.log('Reports updated:', reports);
    }

    /**
     * Export report in specified format
     */
    async exportReport(format) {
        try {
            const data = await window.apiClient.exportReport(format);
            this.downloadFile(data, `keydrop_bot_report.${format}`);
            this.showNotification(`Relatório exportado em ${format.toUpperCase()}`, 'success');
        } catch (error) {
            console.error('Failed to export report:', error);
            this.showNotification('Erro ao exportar relatório', 'error');
        }
    }

    /**
     * Download file helper
     */
    downloadFile(data, filename) {
        const blob = new Blob([typeof data === 'string' ? data : JSON.stringify(data, null, 2)], {
            type: 'application/octet-stream'
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    /**
     * Show notification to user
     */
    showNotification(message, type = 'info') {
        // Play sound notification
        this.playSound(type);
        
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        `;

        // Add to container
        let container = document.getElementById('notificationContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'notificationContainer';
            container.className = 'notification-container';
            document.body.appendChild(container);
        }

        container.appendChild(notification);

        // Setup close button
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            notification.remove();
        });

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    /**
     * Play sound notification
     */
    playSound(type) {
        if (!this.soundEnabled || !this.sounds[type]) return;

        // Initialize audio context if not already done
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }

        const { frequency, duration } = this.sounds[type];
        const oscillator = this.audioContext.createOscillator();
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(frequency, this.audioContext.currentTime);
        oscillator.connect(this.audioContext.destination);
        oscillator.start();
        oscillator.stop(this.audioContext.currentTime + duration / 1000);
    }

    /**
     * Cleanup resources
     */
    destroy() {
        // Clear intervals
        this.updateIntervals.forEach(interval => clearInterval(interval));
        this.updateIntervals.clear();

        // Disconnect WebSocket
        window.apiClient.disconnect();

        this.isInitialized = false;
    }
}

// Export singleton instance
window.uiManager = new UIManager();
