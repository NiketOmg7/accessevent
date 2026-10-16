# AccessEvent — инклюзивная платформа мероприятий

Веб-платформа для организации мероприятий, доступная людям с нарушениями слуха: визуальные уведомления вместо звуковых, текстовый чат, цветовая индикация статусов, тёмная тема.

## Стек технологий

| Слой | Технология |
|---|---|
| Backend | Python 3.11, Flask |
| База данных | PostgreSQL 16 |
| Frontend | HTML5, CSS3, JavaScript, Jinja2 |
| Тестирование | pytest (14 тестов) |
| CI/CD | GitHub Actions |
| Контейнеризация | Docker, docker compose, GHCR |

## Как запустить

### Вариант 1. Docker (рекомендуется)

Открыть: http://localhost:5002

Остановить:

### Вариант 2. Локально

1. Скопировать `.env.example` в `.env` и заполнить:
   - `SECRET_KEY=<случайная строка>`
   - `DATABASE_URL=postgresql://mariaafanaseva@localhost:5432/accessevent`
2. Установить зависимости: `pip install -r requirements.txt`
3. Запустить: `python app.py` (по умолчанию порт 5001)

## Тесты

14 тестов: 6 тестов моделей + 8 тестов API.

## Структура проекта
accessevent/
├── app.py # точка входа, маршруты страниц
├── config.py # конфигурация (SQLite при TESTING)
├── models.py # SQLAlchemy-модели (User, Event, Registration)
├── routes/ # Blueprint'ы
│ ├── auth.py # /api/register, /api/login, /api/profile
│ ├── events.py # /api/events (CRUD)
│ └── registrations.py# /api/registrations
├── utils/
│ ├── auth_helpers.py # JWT, хеширование, декораторы
│ └── accessibility.py# форматирование инклюзивных полей
├── templates/ # Jinja2-шаблоны (6 файлов)
├── static/css, static/js
├── tests/ # pytest (14 тестов)
├── docs/ # вся документация
├── Dockerfile
└── docker-compose.yml

## Документация

- `docs/test_cases.md` — тест-кейсы
- `docs/bug_reports.md` — баг-репорты (3 шт.)
- `docs/user_manual.md` — руководство пользователя
- `docs/admin_manual.md` — руководство администратора
- `docs/api.md` — описание API
- `docs/assessment.md` — SWOT-анализ и направления модернизации

## Docker-образ

Образ публикуется автоматически при push:

## Автор

**Тулинов Никита**, учебная практика ПМ.05, 3 семестр.