FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install poetry
RUN apt-get update && apt-get -y install curl python3-dev
RUN curl -sSL https://install.python-poetry.org --output /tmp/install-poetry.py \
    && POETRY_HOME=/usr/local python3 /tmp/install-poetry.py

# Install dependencies for python packages
RUN apt-get update && apt-get install -y \
  # Pillow
  libjpeg-dev zlib1g-dev libatlas-base-dev \
  # cffi
  libffi-dev \
  # bcrypt
  build-essential cargo \
  # Opencv
  ffmpeg libsm6 libxext6 libgl1

# Install project dependencies
WORKDIR /project
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

# Copy the rest of the project source in
COPY portrayt portrayt