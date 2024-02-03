# Production Dockerfile for application

FROM node:20-bookworm-slim AS frontend

WORKDIR /app

# Asset requirements

COPY ./package.json /app/package.json

COPY ./package-lock.json /app/package-lock.json

RUN npm install

# Build assets

COPY . /app

ENV NODE_ENV=production

RUN npm run build

# Python

FROM python:3.12.1-bookworm AS backend

ENV PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

# Python requirements

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

# Download NLTK files

COPY ./nltk.txt /app/nltk.txt

RUN xargs -I{} python -c "import nltk; nltk.download('{}')" < /app/nltk.txt

# Copy over files

COPY . /app

# Build and copy over assets

COPY --from=frontend /app/static /app/static

# Collect static files for Whitenoise

RUN python manage.py collectstatic --no-input --traceback
