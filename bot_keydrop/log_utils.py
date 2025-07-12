from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from log_utils import setup_logger  # type: ignore

__all__ = ["setup_logger"]
