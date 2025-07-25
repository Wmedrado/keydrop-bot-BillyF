(function(global) {
  const translations = {
    pt: {
      UI_INIT_ERROR: 'Erro ao inicializar interface',
      DATA_LOAD_ERROR: 'Erro ao carregar dados iniciais',
      EMERGENCY_STOP_ACTIVATED: 'Parada de emergência ativada!',
      EMERGENCY_STOP_ERROR: 'Erro na parada de emergência',
      BOT_START_SUCCESS: 'Bot iniciado com sucesso!',
      BOT_START_ERROR: 'Erro ao iniciar o bot',
      BOT_STOP_SUCCESS: 'Bot parado com sucesso!',
      BOT_STOP_ERROR: 'Erro ao parar o bot',
      CONFIG_SAVE_SUCCESS: 'Configuração salva com sucesso!',
      CONFIG_SAVE_ERROR: 'Erro ao salvar configuração',
      CONFIG_RESET_SUCCESS: 'Configuração resetada com sucesso!',
      CONFIG_RESET_ERROR: 'Erro ao resetar configuração',
      CACHE_CLEARED_SUCCESS: 'Cache limpo com sucesso! Logins mantidos.',
      CACHE_CLEARED_ERROR: 'Erro ao limpar cache',
      UPDATE_AVAILABLE: 'Nova versão disponível! Visite o GitHub para baixar.',
      UPDATE_CHECK_ERROR: 'Erro ao verificar atualizações',
      REPORTS_UPDATE_ERROR: 'Erro ao atualizar relatórios',
      REPORT_EXPORT_ERROR: 'Erro ao exportar relatório',
      CANNOT_CONNECT_BACKEND: 'Não foi possível conectar ao backend. Verifique se o servidor está executando.',
      UNEXPECTED_ERROR_APP: 'Erro inesperado na aplicação',
      BACKEND_CONNECTION_LOST: 'Conexão com o backend perdida. Verifique o servidor.',
      CONNECTION_STATUS_CONNECTED: 'Conectado',
      CONNECTION_STATUS_DISCONNECTED: 'Desconectado',
      CONNECTION_STATUS_ERROR: 'Erro de Conexão',
      CONNECTION_STATUS_UNKNOWN: 'Desconhecido',
      LOADING_HEADER: 'Carregando Keydrop Bot Professional',
      LOADING_MESSAGE: 'Conectando ao servidor...',
      INIT_ERROR_HEADER: 'Erro ao Inicializar',
      RETRY_BUTTON: 'Tentar Novamente',
      TEST_UNKNOWN: 'Teste desconhecido',
      TEST_COMPLETED: 'Teste concluído',
      DIAGNOSIS_ERROR: 'Erro no diagnóstico',
      TEACH_AI_COMPLETED: 'Modo de ensino concluído',
      TEACH_AI_ERROR: 'Erro no modo de ensino',
      START_RECORDING: 'Gravação iniciada',
      PAUSE_RECORDING: 'Gravação pausada',
      ERROR_START_RECORDING: 'Erro ao iniciar gravação',
      ERROR_PAUSE_RECORDING: 'Erro ao pausar gravação',
      ERROR_SAVE_MACRO: 'Erro ao salvar macro',
      MACRO_SAVED: 'Macro salva',
      TEACH_AI_TITLE: 'Ensinar IA',
      TEACH_AI_BODY: '<p>Após clicar em iniciar, uma guia será aberta.</p><p>Realize manualmente a participação do sorteio e feche a janela para finalizar.</p>',
      TEACH_AI_START_BUTTON: 'Iniciar'
    },
    en: {
      UI_INIT_ERROR: 'Failed to initialize interface',
      DATA_LOAD_ERROR: 'Failed to load initial data',
      EMERGENCY_STOP_ACTIVATED: 'Emergency stop activated!',
      EMERGENCY_STOP_ERROR: 'Emergency stop failed',
      BOT_START_SUCCESS: 'Bot started successfully!',
      BOT_START_ERROR: 'Failed to start bot',
      BOT_STOP_SUCCESS: 'Bot stopped successfully!',
      BOT_STOP_ERROR: 'Failed to stop bot',
      CONFIG_SAVE_SUCCESS: 'Configuration saved successfully!',
      CONFIG_SAVE_ERROR: 'Failed to save configuration',
      CONFIG_RESET_SUCCESS: 'Configuration reset successfully!',
      CONFIG_RESET_ERROR: 'Failed to reset configuration',
      CACHE_CLEARED_SUCCESS: 'Cache cleared successfully! Logins kept.',
      CACHE_CLEARED_ERROR: 'Failed to clear cache',
      UPDATE_AVAILABLE: 'New version available! Visit GitHub to download.',
      UPDATE_CHECK_ERROR: 'Failed to check for updates',
      REPORTS_UPDATE_ERROR: 'Failed to update reports',
      REPORT_EXPORT_ERROR: 'Failed to export report',
      CANNOT_CONNECT_BACKEND: 'Could not connect to backend. Make sure the server is running.',
      UNEXPECTED_ERROR_APP: 'Unexpected application error',
      BACKEND_CONNECTION_LOST: 'Connection to backend lost. Check the server.',
      CONNECTION_STATUS_CONNECTED: 'Connected',
      CONNECTION_STATUS_DISCONNECTED: 'Disconnected',
      CONNECTION_STATUS_ERROR: 'Connection Error',
      CONNECTION_STATUS_UNKNOWN: 'Unknown',
      LOADING_HEADER: 'Loading Keydrop Bot Professional',
      LOADING_MESSAGE: 'Connecting to server...',
      INIT_ERROR_HEADER: 'Initialization Error',
      RETRY_BUTTON: 'Try Again',
      TEST_UNKNOWN: 'Unknown test',
      TEST_COMPLETED: 'Test completed',
      DIAGNOSIS_ERROR: 'Diagnosis error',
      TEACH_AI_COMPLETED: 'Teaching mode completed',
      TEACH_AI_ERROR: 'Teaching mode error',
      START_RECORDING: 'Recording started',
      PAUSE_RECORDING: 'Recording paused',
      ERROR_START_RECORDING: 'Failed to start recording',
      ERROR_PAUSE_RECORDING: 'Failed to pause recording',
      ERROR_SAVE_MACRO: 'Failed to save macro',
      MACRO_SAVED: 'Macro saved',
      TEACH_AI_TITLE: 'Teach AI',
      TEACH_AI_BODY: '<p>After clicking start, a tab will open.</p><p>Manually perform the giveaway participation and close the window to finish.</p>',
      TEACH_AI_START_BUTTON: 'Start'
    },
    es: {
      UI_INIT_ERROR: 'Error al iniciar la interfaz',
      DATA_LOAD_ERROR: 'Error al cargar datos iniciales',
      EMERGENCY_STOP_ACTIVATED: '¡Parada de emergencia activada!',
      EMERGENCY_STOP_ERROR: 'Error en la parada de emergencia',
      BOT_START_SUCCESS: '¡Bot iniciado con éxito!',
      BOT_START_ERROR: 'Error al iniciar el bot',
      BOT_STOP_SUCCESS: '¡Bot detenido con éxito!',
      BOT_STOP_ERROR: 'Error al detener el bot',
      CONFIG_SAVE_SUCCESS: '¡Configuración guardada con éxito!',
      CONFIG_SAVE_ERROR: 'Error al guardar la configuración',
      CONFIG_RESET_SUCCESS: '¡Configuración reiniciada con éxito!',
      CONFIG_RESET_ERROR: 'Error al reiniciar la configuración',
      CACHE_CLEARED_SUCCESS: 'Caché limpiada con éxito. Sesiones conservadas.',
      CACHE_CLEARED_ERROR: 'Error al limpiar la caché',
      UPDATE_AVAILABLE: '¡Nueva versión disponible! Visite GitHub para descargar.',
      UPDATE_CHECK_ERROR: 'Error al verificar actualizaciones',
      REPORTS_UPDATE_ERROR: 'Error al actualizar informes',
      REPORT_EXPORT_ERROR: 'Error al exportar informe',
      CANNOT_CONNECT_BACKEND: 'No se pudo conectar con el backend. Asegúrese de que el servidor esté en ejecución.',
      UNEXPECTED_ERROR_APP: 'Error inesperado de la aplicación',
      BACKEND_CONNECTION_LOST: 'Conexión con el backend perdida. Verifique el servidor.',
      CONNECTION_STATUS_CONNECTED: 'Conectado',
      CONNECTION_STATUS_DISCONNECTED: 'Desconectado',
      CONNECTION_STATUS_ERROR: 'Error de conexión',
      CONNECTION_STATUS_UNKNOWN: 'Desconocido',
      LOADING_HEADER: 'Cargando Keydrop Bot Professional',
      LOADING_MESSAGE: 'Conectando al servidor...',
      INIT_ERROR_HEADER: 'Error al iniciar',
      RETRY_BUTTON: 'Intentar de nuevo',
      TEST_UNKNOWN: 'Prueba desconocida',
      TEST_COMPLETED: 'Prueba completada',
      DIAGNOSIS_ERROR: 'Error en el diagnóstico',
      TEACH_AI_COMPLETED: 'Modo de enseñanza completado',
      TEACH_AI_ERROR: 'Error en el modo de enseñanza',
      START_RECORDING: 'Grabación iniciada',
      PAUSE_RECORDING: 'Grabación pausada',
      ERROR_START_RECORDING: 'Error al iniciar la grabación',
      ERROR_PAUSE_RECORDING: 'Error al pausar la grabación',
      ERROR_SAVE_MACRO: 'Error al guardar la macro',
      MACRO_SAVED: 'Macro guardada',
      TEACH_AI_TITLE: 'Enseñar IA',
      TEACH_AI_BODY: '<p>Después de hacer clic en iniciar, se abrirá una pestaña.</p><p>Realiza manualmente la participación en el sorteo y cierra la ventana para finalizar.</p>',
      TEACH_AI_START_BUTTON: 'Iniciar'
    }
  };

  let currentLanguage = localStorage.getItem('language') || 'pt';

  function t(key) {
    return (translations[currentLanguage] && translations[currentLanguage][key]) ||
           (translations.pt && translations.pt[key]) ||
           key;
  }

  function setLanguage(lang) {
    if (translations[lang]) {
      currentLanguage = lang;
      localStorage.setItem('language', lang);
    }
  }

  function getLanguage() {
    return currentLanguage;
  }

  global.i18n = { t, setLanguage, getLanguage };
})(this);
