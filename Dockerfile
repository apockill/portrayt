FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies for python packages
RUN apt-get update && apt-get install -y \
  curl python3-dev \
  # Pillow
  libjpeg-dev zlib1g-dev libatlas-base-dev \
  # cffi
  libffi-dev \
  # bcrypt
  build-essential cargo \
  # Opencv
  ffmpeg libsm6 libxext6 libgl1 \
  # Cryptography build (on arm 32 platform)
  libssl-dev python3-venv

RUN curl -sSL https://install.python-poetry.org --output /tmp/install-poetry.py \
    && POETRY_HOME=/usr/local python3 /tmp/install-poetry.py

# Install project dependencies
WORKDIR /project
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-dev

# Copy the rest of the project source in
COPY portrayt portrayt