#!/bin/bash
set -e
mkdir -p build_results tests

# Install python dependencies
pip install -r bot_keydrop/requirements.txt

pip install -r bot_keydrop/backend/requirements.txt || true
# Ensure critical backend deps are installed even if optional ones fail
pip install firebase_admin discord-webhook || true
pip install pytest pytest-asyncio pytest-mock pytest-cov pytest-html flake8 black
# Backend requirements contain heavy packages not needed for tests
# so we avoid installing them to speed up CI
pip install beautifulsoup4
pip install pytest pytest-asyncio pytest-mock pytest-cov pytest-html flake8 black tkhtmlview

# Validate modifications to protected files
python ci/check_protected_files.py | tee build_results/protected_files.log


# Lint with flake8 and black
flake8 . > build_results/flake8.log || true
black --check . > build_results/black.log || true


# Semantic naming validation
python ci/check_naming_quality.py | tee build_results/naming_quality.log

# Validate PR checklist
python ci/pr_validation.py


# Dependency check
python - <<'PY'
from bot_keydrop.system_safety import run_dependency_check
if not run_dependency_check():
    print("Dependency check failed, continuing anyway")
PY

# Run tests with coverage and html report
pytest --html=tests/test_report.html --self-contained-html --cov=bot_keydrop --cov-report=term --cov-report=html:tests/htmlcov | tee tests/coverage.txt

# Regression intelligence validation
python ci/check_regression_intelligence.py | tee build_results/regression_check.log
# Automated PR review
python ci/auto_pr_review.py | tee build_results/auto_review.log

echo "Build succeeded" > build_results/build_status.log
