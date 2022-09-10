#!/bin/bash
set -euxo pipefail

poetry run isort portrayt/ tests/
poetry run black portrayt/ tests/
