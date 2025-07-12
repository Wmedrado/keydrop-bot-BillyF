/**
 * UI Manager for Keydrop Bot Professional
 * Handles all user interface interactions and updates
 */

class UIManager {
    constructor() {
        this.t = window.i18n ? window.i18n.t : (k => k);
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
        this.handleProxyChange = this.handleProxyChange.bind(this);
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
            this.showNotification(this.t('UI_INIT_ERROR'), 'error');
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

        const langSelect = document.getElementById('languageSelect');
        if (langSelect) {
            langSelect.value = window.i18n.getLanguage();
            langSelect.addEventListener('change', (e) => {
                window.i18n.setLanguage(e.target.value);
                this.updateConnectionStatus();
            });
        }

        // Configuration form elements
        this.setupConfigEventListeners();

        // Control buttons
        this.setupControlEventListeners();

        // Reports and exports
        this.setupReportsEventListeners();

        // Diagnostics buttons
        this.setupDiagnosticsEventListeners();

        // Contingency panel
        this.setupContingencyEventListeners();
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
        const teachAIBtn = document.getElementById('teachAIBtn');
        const testDiscordBtn = document.getElementById('testDiscordBtn');

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

        if (teachAIBtn) {
            teachAIBtn.addEventListener('click', () => {
                this.showTeachAIModal();
            });
        }

        if (testDiscordBtn) {
            testDiscordBtn.addEventListener('click', () => {
                this.runDiagnostic('notification');
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

    setupDiagnosticsEventListeners() {
        const keydropBtn = document.getElementById('testKeydropBtn');
        const loginBtn = document.getElementById('testLoginBtn');
        const notifBtn = document.getElementById('testNotificationBtn');
        const proxyBtn = document.getElementById('testProxyBtn');

        if (keydropBtn) keydropBtn.addEventListener('click', () => this.runDiagnostic('keydrop'));
        if (loginBtn) loginBtn.addEventListener('click', () => this.runDiagnostic('login'));
        if (notifBtn) notifBtn.addEventListener('click', () => this.runDiagnostic('notification'));
        if (proxyBtn) {
            proxyBtn.addEventListener('click', () => {
                const proxy = prompt('Proxy (ex: http://usuario:senha@ip:porta)');
                if (proxy) this.runDiagnostic('proxy', { proxy });
            });
        }
    }

    setupContingencyEventListeners() {
        const list = document.getElementById('contingencyList');
        if (list) {
            list.addEventListener('click', (e) => {
                const li = e.target.closest('li');
                if (!li) return;
                if (e.target.classList.contains('up-btn') && li.previousElementSibling) {
                    list.insertBefore(li, li.previousElementSibling);
                } else if (e.target.classList.contains('down-btn') && li.nextElementSibling) {
                    list.insertBefore(li.nextElementSibling, li);
                }
            });
        }

        const recBtn = document.getElementById('recordMacroBtn');
        const pauseBtn = document.getElementById('pauseMacroBtn');
        const saveBtn = document.getElementById('saveMacroBtn');

        if (recBtn) recBtn.addEventListener('click', () => this.startMacro());
        if (pauseBtn) pauseBtn.addEventListener('click', () => this.pauseMacro());
        if (saveBtn) saveBtn.addEventListener('click', () => this.saveMacro());
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
            this.showNotification(this.t('DATA_LOAD_ERROR'), 'error');
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

        if (id === 'numTabs') {
            this.renderProxyInputs();
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

    handleProxyChange(event) {
        const { dataset, value } = event.target;
        const tabId = parseInt(dataset.tabId, 10);
        if (!this.config.tab_proxies) {
            this.config.tab_proxies = {};
        }
        if (value) {
            this.config.tab_proxies[tabId] = value;
        } else {
            delete this.config.tab_proxies[tabId];
        }
        this.markConfigModified();
    }

    /**
     * Handle emergency stop
     */
    async handleEmergencyStop() {
        try {
            await window.apiClient.emergencyStop();
            this.showNotification(this.t('EMERGENCY_STOP_ACTIVATED'), 'warning');
            this.playSound('emergency');
        } catch (error) {
            console.error('Emergency stop failed:', error);
            this.showNotification(this.t('EMERGENCY_STOP_ERROR'), 'error');
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
            this.showNotification(this.t('BOT_START_SUCCESS'), 'success');
            this.playSound('success');

        } catch (error) {
            console.error('Failed to start bot:', error);
            this.showNotification(this.t('BOT_START_ERROR'), 'error');
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
            this.showNotification(this.t('BOT_STOP_SUCCESS'), 'success');
            this.playSound('success');

        } catch (error) {
            console.error('Failed to stop bot:', error);
            this.showNotification(this.t('BOT_STOP_ERROR'), 'error');
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
            this.showNotification(this.t('CONFIG_SAVE_SUCCESS'), 'success');

            if (saveBtn) {
                saveBtn.classList.remove('modified');
                saveBtn.textContent = 'Configuração Salva';
            }

        } catch (error) {
            console.error('Failed to save config:', error);
            this.showNotification(this.t('CONFIG_SAVE_ERROR'), 'error');
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
            this.showNotification(this.t('CONFIG_RESET_SUCCESS'), 'success');
        } catch (error) {
            console.error('Failed to reset config:', error);
            this.showNotification(this.t('CONFIG_RESET_ERROR'), 'error');
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
                this.showNotification(this.t('CACHE_CLEARED_SUCCESS'), 'success');
            } else {
                this.showNotification(this.t('CACHE_CLEARED_ERROR'), 'error');
            }

        } catch (error) {
            console.error('Failed to clear cache:', error);
            this.showNotification(this.t('CACHE_CLEARED_ERROR'), 'error');
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
                this.showNotification(this.t('UPDATE_AVAILABLE'), 'info');
            }

        } catch (error) {
            console.error('Failed to check for updates:', error);
            this.showNotification(this.t('UPDATE_CHECK_ERROR'), 'error');
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

        this.renderProxyInputs();
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
            this.showNotification(this.t('REPORTS_UPDATE_ERROR'), 'error');
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
            this.showNotification(this.t('REPORT_EXPORT_ERROR'), 'error');
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

    async runDiagnostic(type, payload = {}) {
        const output = document.getElementById('diagnosticsOutput');
        if (output) {
            output.textContent = 'Executando teste...';
        }
        try {
            let result;
            switch (type) {
                case 'keydrop':
                    result = await window.apiClient.testKeydrop();
                    break;
                case 'login':
                    result = await window.apiClient.testLogin();
                    break;
                case 'notification':
                    result = await window.apiClient.testNotification();
                    break;
                case 'proxy':
                    result = await window.apiClient.testProxy(payload.proxy);
                    break;
                default:
                    result = { success: false, message: 'Teste desconhecido' };
            }
            if (output) {
                output.textContent = JSON.stringify(result, null, 2);
            }
            this.showNotification(result.message || 'Teste concluído', result.success ? 'success' : 'error');
        } catch (error) {
            if (output) {
                output.textContent = error.message;
            }
            this.showNotification('Erro no diagnóstico', 'error');
        }
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

    showTeachAIModal() {
        const overlay = document.getElementById('modalOverlay');
        const title = document.getElementById('modalTitle');
        const body = document.getElementById('modalBody');
        const footer = document.getElementById('modalFooter');
        const closeBtn = document.getElementById('modalClose');
        if (!overlay) return;

        title.textContent = 'Ensinar IA';
        body.innerHTML = '<p>Após clicar em iniciar, uma guia será aberta.</p><p>Realize manualmente a participação do sorteio e feche a janela para finalizar.</p>';
        footer.innerHTML = '<button id="startTeachAI">Iniciar</button>';
        overlay.style.display = 'block';

        document.getElementById('startTeachAI').addEventListener('click', async () => {
            overlay.style.display = 'none';
            try {
                await window.apiClient.teachAI();
                this.showNotification('Modo de ensino concluído', 'success');
            } catch (err) {
                this.showNotification('Erro no modo de ensino', 'error');
            }
        });

        if (closeBtn) {
            closeBtn.onclick = () => { overlay.style.display = 'none'; };
        }
    }

    async startMacro() {
        try {
            await window.apiClient.startMacro(1);
            this.showNotification('Gravação iniciada', 'success');
        } catch (err) {
            this.showNotification('Erro ao iniciar gravação', 'error');
        }
    }

    async pauseMacro() {
        try {
            await window.apiClient.pauseMacro(1);
            this.showNotification('Gravação pausada', 'info');
        } catch (err) {
            this.showNotification('Erro ao pausar gravação', 'error');
        }
    }

    async saveMacro() {
        const useFirst = document.getElementById('useMacroFirst')?.checked || false;
        try {
            await window.apiClient.saveMacro(1, useFirst);
            this.showNotification('Macro salva', 'success');
        } catch (err) {
            this.showNotification('Erro ao salvar macro', 'error');
        }
    }

    renderProxyInputs() {
        const container = document.getElementById('proxyList');
        if (!container) return;
        container.innerHTML = '';
        const numTabs = this.config.numTabs || 0;
        if (this.config.tab_proxies) {
            Object.keys(this.config.tab_proxies).forEach(key => {
                if (parseInt(key) > numTabs) {
                    delete this.config.tab_proxies[key];
                }
            });
        }
        for (let i = 1; i <= numTabs; i++) {
            const wrapper = document.createElement('div');
            wrapper.className = 'form-group full-width';
            const label = document.createElement('label');
            label.textContent = `Guia ${i} Proxy`;
            const input = document.createElement('input');
            input.type = 'text';
            input.dataset.tabId = i;
            input.value = this.config.tab_proxies && this.config.tab_proxies[i] ? this.config.tab_proxies[i] : '';
            input.addEventListener('input', this.handleProxyChange);
            wrapper.appendChild(label);
            wrapper.appendChild(input);
            container.appendChild(wrapper);
        }
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
