# Руководство администратора AccessEvent

## 1. Системные требования
- Python 3.11+
- PostgreSQL 15+
- Docker 24+

## 2. Развёртывание

### Локально:
1. python -m venv venv
2. pip install -r requirements.txt
3. Настроить .env
4. python app.py (порт 5001)

### Контейнерно:
docker compose up -d
docker compose down

## 3. Переменные окружения (.env)
| Переменная | Назначение | Пример |
|---|---|---|
| DATABASE_URL | Подключение к PostgreSQL | postgresql://user:pass@localhost:5432/accessevent |
| SECRET_KEY | Ключ подписи JWT | длинная случайная строка |
| TESTING | Переключение на SQLite (только тесты) | 1 |

## 4. Роли и права
| Роль | Права |
|---|---|
| participant | регистрация на мероприятия, просмотр |
| organizer | всё participant + создание/редактирование мероприятий |
| admin | всё organizer + удаление |

## 5. Резервное копирование
pg_dump -U postgres accessevent > backup.sql
psql -U postgres accessevent < backup.sql

## 6. Типовые проблемы
1. Password authentication failed — неверный пароль в .env
2. Connection refused — не запущен PostgreSQL
3. Address already in use (порт 5001) — старый процесс не завершён
4. Таблицы не создаются — проверьте вызов db.create_all() в app.py
5. Контейнер web падает — неверный DATABASE_URL в docker-compose.yml (хост db, не localhost)
