# portrayt
This project combines e-paper, raspberry pi's, and StableDiffusion to make a picture frame that portrays anything you ask of it.
_________________

[![PyPI version](https://badge.fury.io/py/portrayt.svg)](http://badge.fury.io/py/portrayt)
[![Test Status](https://github.com/apockill/portrayt/workflows/Test/badge.svg?branch=main)](https://github.com/apockill/portrayt/actions?query=workflow%3ATest)
[![Lint Status](https://github.com/apockill/portrayt/workflows/Lint/badge.svg?branch=main)](https://github.com/apockill/portrayt/actions?query=workflow%3ALint)
[![codecov](https://codecov.io/gh/apockill/portrayt/branch/main/graph/badge.svg)](https://codecov.io/gh/apockill/portrayt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)
_________________

[Read Latest Documentation](https://apockill.github.io/portrayt/) - [Browse GitHub Code Repository](https://github.com/apockill/portrayt/)
_________________

## Development

### Installing python dependencies
```shell
poetry install
```

### Running Tests
```shell
pytest .
```

### Formatting Code
```shell
bash .github/format.sh
```

### Linting
```shell
bash .github/check_lint.sh
```

## Running the Program
Install docker
```bash
curl -sSL https://get.docker.com | sh
```

Create a .env file in your current directory and fill in the API key:
```bash
REPLICATE_API_TOKEN=<your token here>
```

Build and run the image
```bash
docker compose up --build -d
```