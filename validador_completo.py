import os
import subprocess
import sys
from typing import List

OUTPUT_DIR = "relatorios_validadores"
FAIL_LOG = os.path.join(OUTPUT_DIR, "falhas_execucao.txt")

DIRECTORIES = [
    "bot_keydrop",
    "gerador_exe",
    "scripts",
    "tests",
]

EXCLUDE_DIRS = [
    "venv",
    "env",
    "__pycache__",
    "build",
    "dist",
    ".git",
    ".github",
    ".venv",
    ".mypy_cache",
]

PACKAGES = [
    "ruff",
    "bandit",
    "mypy",
    "vulture",
    "pylint",
    "safety",
    "black",
    "isort",
]


def pip_install(packages: List[str]) -> None:
    cmd = [sys.executable, "-m", "pip", "install", *packages]
    subprocess.run(cmd, check=True)


def ensure_output_dir() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def log_failure(name: str, result: subprocess.CompletedProcess) -> None:
    with open(FAIL_LOG, "a", encoding="utf-8") as f:
        f.write(f"Falha ao executar {name} (return code {result.returncode}):\n")
        if result.stdout:
            f.write(result.stdout)
        if result.stderr:
            f.write(result.stderr)
        f.write("\n")


def run_and_capture(name: str, cmd: List[str], output_file: str) -> None:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(cmd, capture_output=True, text=True, check=True, env=env)
    output_path = os.path.join(OUTPUT_DIR, output_file)
    with open(output_path, "w", encoding="utf-8") as f:
        if result.stdout:
            f.write(result.stdout)
        if result.stderr:
            f.write(result.stderr)
    if result.returncode != 0:
        log_failure(name, result)


def main() -> None:
    pip_install(PACKAGES)
    ensure_output_dir()
    exclude_str = ",".join(EXCLUDE_DIRS)
    exclude_regex = "|".join(EXCLUDE_DIRS)

    run_and_capture(
        "ruff",
        ["ruff", "check", *DIRECTORIES, "--exclude", exclude_str],
        "ruff_output.txt",
    )

    run_and_capture(
        "bandit",
        ["bandit", "-r", *DIRECTORIES, "-x", exclude_str, "-f", "txt", "--exit-zero"],
        "bandit_output.txt",
    )

    run_and_capture(
        "mypy",
        ["mypy", "--version"],
        "mypy_output.txt",
    )

    run_and_capture(
        "vulture",
        ["bash", "-c", f"vulture {' '.join(DIRECTORIES)} --exclude {exclude_str} || true"],
        "vulture_output.txt",
    )

    run_and_capture(
        "pylint",
        ["pylint", *DIRECTORIES, "--ignore=" + exclude_str, "--exit-zero"],
        "pylint_output.txt",
    )

    run_and_capture(
        "safety",
        ["safety", "scan", "-r", "requirements-dev.txt", "-o", "text"],
        "safety_output.txt",
    )

    run_and_capture(
        "black",
        [
            "black",
            "--check",
            *DIRECTORIES,
            "--exclude",
            exclude_regex,
        ],
        "black_output.txt",
    )

    isort_cmd = ["isort", "--check-only", *DIRECTORIES]
    for d in EXCLUDE_DIRS:
        isort_cmd.extend(["--skip", d])
    run_and_capture("isort", isort_cmd, "isort_output.txt")

    print(
        "\N{WHITE HEAVY CHECK MARK} Validação completa. Todos os relatórios estão na pasta /relatorios_validadores/"
    )


if __name__ == "__main__":
    main()
