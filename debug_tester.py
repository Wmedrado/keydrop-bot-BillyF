from __future__ import annotations

import logging
import subprocess
import sys
import time
from pathlib import Path

from log_utils import setup_logger


def run_pytest(logger: logging.Logger) -> bool:
    """Run the project's pytest suite and log the results."""
    if not hasattr(logger, "info"):
        raise TypeError("logger must have 'info' method")
    start = time.time()
    logger.info("Executando suite de testes com pytest")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"], capture_output=True, text=True
    )
    duration = time.time() - start
    logger.info("Saida pytest:\n%s", result.stdout + result.stderr)
    logger.info("Tempo pytest: %.2fs", duration)
    return result.returncode == 0


def check_assets(logger: logging.Logger) -> bool:
    """Verify required asset files are present."""
    if not hasattr(logger, "info"):
        raise TypeError("logger must have 'info' method")
    assets = [
        Path("bot_keydrop/backend"),
        Path("bot_keydrop/frontend"),
        Path("bot-icone.ico"),
    ]
    ok = True
    for path in assets:
        if path.exists():
            logger.info("Asset presente: %s", path)
        else:
            logger.error("Asset ausente: %s", path)
            ok = False
    return ok


def main() -> None:
    """Entry point used when running the executable in debug mode."""
    logs_dir = Path("logs")
    logger = setup_logger("debug_relatorio", logs_dir=str(logs_dir))
    logger.info("=== MODO DEBUG INICIADO ===")

    tests_ok = run_pytest(logger)
    assets_ok = check_assets(logger)

    if tests_ok and assets_ok:
        logger.info("Resultado final: SUCESSO")
    else:
        logger.error("Resultado final: FALHAS DETECTADAS")


if __name__ == "__main__":
    main()
