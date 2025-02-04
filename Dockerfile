FROM python:3.11-slim


WORKDIR /usr/src/app


ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client libpq-dev gcc libc6-dev zlib1g-dev libjpeg-dev libffi-dev libssl-dev \
    libfreetype6-dev libjpeg62-turbo-dev libpango1.0-dev libcairo2-dev \
    gettext libgettextpo-dev fonts-dejavu libgdk-pixbuf2.0-dev libpango-1.0-0 libpangocairo-1.0-0 \
    nodejs npm redis-server \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .