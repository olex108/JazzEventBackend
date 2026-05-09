# --- ЭТАП 1: Сборка Фронтенда (Vite) ---
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./

RUN npm install

COPY frontend/ ./

COPY templates/ ../templates/

RUN npm run build  # Создает папку /app/frontend/dist


# ЭТАП 2: Сборка Django
# Указываем базовый образ
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    libpq-dev \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Копируем файл с зависимостями и устанавливаем их
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости с помощью Poetry
RUN poetry install --no-root --no-interaction --no-ansi

# Копируем остальные файлы проекта в контейнер
COPY . .

# !!! ГЛАВНЫЙ МОМЕНТ: Забираем собранный фронтенд из первого этапа
# Копируем из frontend-builder (папка dist) в папку, где её ждет Django
COPY frontend/dist /app/static/dist

RUN mkdir -p /app/logs

# Теперь можно запустить collectstatic прямо ПРИ СБОРКЕ образа
# Чтобы на сервер статика уехала уже внутри образа
RUN python manage.py collectstatic --noinput

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Копируем entrypoint.sh и даем права
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Определяем команду для запуска приложения
ENTRYPOINT ["/app/entrypoint.sh"]
