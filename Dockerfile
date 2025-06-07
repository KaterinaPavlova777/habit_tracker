FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
        gcc \
        python3-dev \
        libpq-dev \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# Создаём пользователя (с проверкой на существование)
RUN set -xe \
    && id -u appuser >/dev/null 2>&1 || useradd -m -u 1000 appuser

WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY . .

# Настройка прав
RUN chown -R appuser:appuser /app
USER appuser

# Команда запуска
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi"]