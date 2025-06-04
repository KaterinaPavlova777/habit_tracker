# Используем официальный образ Python
FROM python:3.12-slim

# Создаём пользователя для безопасности
RUN useradd -m -u 1000 appuser

# Устанавливаем рабочую директорию
WORKDIR /app

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