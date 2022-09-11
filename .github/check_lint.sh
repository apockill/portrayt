#!/bin/bash
set -euxo pipefail

poetry run cruft check
poetry run mypy --ignore-missing-imports portrayt/ tests/
poetry run isort --check --diff portrayt/ tests/
poetry run black --check portrayt/ tests/
poetry run flake8 portrayt/ tests/ --darglint-ignore-regex '^test_.*'
poetry run bandit -r --severity high portrayt/ tests/
poetry run vulture --min-confidence 100 portrayt/ tests/
echo "Lint successful!"