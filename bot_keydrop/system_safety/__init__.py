from .environment_checker import (
    verificar_conexao_internet,
    ambiente_compativel,
    verificar_arquivos_obrigatorios,
    LockFile,
    executando_no_diretorio_correto,
)
from .permissions_validator import validar_permissoes
from .backups import backup_arquivo, restaurar_arquivo
from .watchdog import ProcessWatchdog
from .crash_tracker import start_crash_tracker, log_exception
from .error_reporter import error_reporter, ErrorReporter
from .diagnostic import diagnostic
from .dependency_validator import run_dependency_check, get_available_browser
from .browser_fallback import launch_browser_with_fallback
from .rate_limiter import RateLimiter
from .timeout import enforce_timeout, TimeoutException
from .sandbox import run_in_sandbox
from .stability import (
    auto_retry,
    BotWatchdog,
    backup_config,
    snapshot_environment,
    check_crash_and_mark,
    detect_anomalies,
    detect_memory_leak,
    send_log_to_discord,
)

__all__ = [
    "verificar_conexao_internet",
    "ambiente_compativel",
    "verificar_arquivos_obrigatorios",
    "LockFile",
    "executando_no_diretorio_correto",
    "validar_permissoes",
    "backup_arquivo",
    "restaurar_arquivo",
    "ProcessWatchdog",
    "error_reporter",
    "ErrorReporter",
    "diagnostic",
    "run_dependency_check",
    "get_available_browser",
    "enforce_timeout",
    "TimeoutException",
    "run_in_sandbox",
    "auto_retry",
    "BotWatchdog",
    "backup_config",
    "snapshot_environment",
    "check_crash_and_mark",
    "detect_anomalies",
    "detect_memory_leak",
    "send_log_to_discord",
    "start_crash_tracker",
    "log_exception",
    "RateLimiter",
    "launch_browser_with_fallback",
]
