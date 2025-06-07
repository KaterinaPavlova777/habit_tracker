# Habit Tracker

Habit Tracker — это Django-приложение для отслеживания привычек с REST API, интеграцией с Telegram и асинхронной обработкой задач через Celery. Проект использует PostgreSQL для хранения данных, Redis как брокер сообщений и Docker для контейнеризации.

## Требования

Для локального запуска проекта вам понадобятся:
- Python 3.12
- Docker и Docker Compose
- Git
- PostgreSQL 15 (или Docker для запуска базы данных)
- Redis 7 (или Docker для запуска Redis)

## Локальная настройка и запуск

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/KaterinaPavlova777/habit_tracker.git
cd habit_tracker
```

### 2. Настройте переменные окружения
Создайте файл `.env` в корне проекта со следующими переменными:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=habit_tracker
DB_USER=postgres
DB_PASSWORD=123456
DB_HOST=postgres
DB_PORT=5432
SECRET_KEY=your-very-secure-secret-key
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

Замените `SECRET_KEY` и `TELEGRAM_BOT_TOKEN` на ваши значения. Для генерации `SECRET_KEY` можно использовать онлайн-генераторы или команду:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 3. Установите зависимости
Если вы запускаете проект без Docker, установите Python-зависимости:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Запустите сервисы с помощью Docker Compose
Убедитесь, что Docker и Docker Compose установлены. Затем выполните:

```bash
docker-compose -f docker-compose.yml up --build
```

Это запустит:
- Сервис `web` (Django-приложение)
- Сервис `celery` (Celery worker)
- PostgreSQL (`postgres:15`)
- Redis (`redis:7`)

### 5. Примените миграции
В отдельном терминале выполните:

```bash
docker-compose exec web python manage.py migrate
```

### 6. Создайте суперпользователя (опционально)
Для доступа к Django Admin:

```bash
docker-compose exec web python manage.py createsuperuser
```

### 7. Проверьте запуск
Откройте браузер и перейдите по адресу `http://localhost:8000` (порт может отличаться в зависимости от настроек `docker-compose.yml`).

## Тестирование

Проект включает тесты для приложений `habits` и `users`. Чтобы запустить тесты локально:

```bash
docker-compose exec web python manage.py test habits.tests users.tests
```

## Настройка CI/CD с помощью GitHub Actions

Проект использует GitHub Actions для автоматического тестирования, сборки и деплоя. Workflow находится в файле `.github/workflows/ci.yml`.

### 1. Настройте секреты в GitHub
Перейдите в `Settings -> Secrets and variables -> Actions -> New repository secret` и добавьте следующие секреты:

- `DOCKER_USERNAME`: Имя пользователя Docker Hub (например, `doomuy`).
- `DOCKER_PASSWORD`: Пароль или токен доступа для Docker Hub.
- `SERVER_HOST`: IP-адрес или домен сервера для деплоя.
- `SERVER_USERNAME`: Имя пользователя для SSH-доступа к серверу.
- `SERVER_SSH_KEY`: Приватный SSH-ключ для доступа к серверу.
- `SECRET_KEY`: Секретный ключ Django.
- `TELEGRAM_BOT_TOKEN`: Токен Telegram-бота.

### 2. Описание CI/CD pipeline
Workflow выполняет следующие шаги:
- **Тестирование**:
  - Запускает сервисы PostgreSQL и Redis.
  - Устанавливает Python-зависимости из `requirements.txt`.
  - Применяет миграции (`python manage.py migrate`).
  - Запускает тесты (`python manage.py test habits.tests users.tests`).
- **Сборка и пуш**:
  - Собирает Docker-образы для сервисов `web` и `celery` с помощью `docker-compose`.
  - Тегирует образы (`doomuy/habit_tracker-web:latest`, `doomuy/habit_tracker-celery:latest`).
  - Пушит образы в Docker Hub.
- **Деплой**:
  - Подключается к серверу по SSH.
  - Выполняет `docker-compose down`, `docker-compose pull`, и `docker-compose up -d` для обновления приложения.

### 3. Проверка CI/CD
1. Запушьте изменения в ветку `develop`:
   ```bash
   git push origin develop
   ```
2. Перейдите в раздел `Actions` в GitHub, чтобы проверить статус workflow.
3. Убедитесь, что тесты проходят, образы пушатся в Docker Hub, и деплой на сервер завершается успешно.

## Деплой на сервер

### 1. Подготовьте сервер
- Установите Docker и Docker Compose на сервер:
  ```bash
  sudo apt-get update
  sudo apt-get install -y docker.io docker-compose
  sudo systemctl enable docker
  sudo systemctl start docker
  ```
- Настройте SSH-доступ для пользователя (например, `doomuy`):
  ```bash
  ssh-copy-id misskatkaterina@your-server-ip
  ```

### 2. Настройте директорию проекта
Создайте директорию `/home/doomuy/habit_tracker` на сервере и скопируйте `docker-compose.yml`:

```bash
mkdir -p /home/misskatkaterina/habit_tracker
scp docker-compose.yml misskatkaterina@your-server-ip:/home/doomuy/habit_tracker/
```

### 3. Выполните деплой
GitHub Actions автоматически деплоит приложение при пуше в ветку `develop`. Для ручного деплоя на сервере выполните:

```bash
cd /home/doomuy/habit_tracker
docker-compose -f docker-compose.yml down
docker-compose -f docker-compose.yml pull
docker-compose -f docker-compose.yml up -d
```

### 4. Проверьте статус
Проверьте, что сервисы работают:

```bash
docker-compose ps
```

Убедитесь, что приложение доступно по адресу сервера (например, `http://your-server-ip:8000`).

## Устранение неполадок

- **Ошибка миграций**: Если миграции не проходят, проверьте настройки `DATABASES` в `settings.py` и убедитесь, что переменные окружения совпадают с `docker-compose.yml`.
- **Ошибка сборки Docker**: Проверьте `requirements.txt` на конфликты версий и убедитесь, что в `Dockerfile` установлены все системные зависимости (`libpq-dev`, `gcc`).
- **Ошибка деплоя**: Проверьте логи GitHub Actions и убедитесь, что секреты настроены корректно.
