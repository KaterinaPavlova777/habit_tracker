# Используем официальный образ Python
FROM python:3.12-slim

# Создаём пользователя для безопасности
RUN useradd -m -u 1000 appuser

# Устанавливаем рабочую директорию
WORKDIR /appaFROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
        gcc \
        python3-dev \
        libpq-dev \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# Создаём пользователя
RUN useradd -m -u 1000 appuser
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

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Меняем владельца файлов
RUN chown -R appuser:appuser /app

# Переключаемся на пользователя appuser
USER appuser

# Выполняем миграции и запускаем сервер (правильный путь)
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]