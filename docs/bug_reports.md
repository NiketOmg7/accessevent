# Баг-репорты AccessEvent

## BUG-01. [Major] Повторная регистрация с тем же email возвращала 409 без явной проверки
- Серьёзность: Major
- Приоритет: P2
- Шаги воспроизведения:
  1. POST /api/register с email test@mail.ru
  2. POST /api/register ещё раз с тем же email
- Фактический результат: 409 из-за UNIQUE-конфликта без явного сообщения
- Ожидаемый результат: 409 с понятным сообщением
- Статус: Исправлен (добавлена явная проверка `User.query.filter_by(email=email).first()` в routes/auth.py)

## BUG-02. [Major] Регистрация принимала email без @
- Серьёзность: Major
- Приоритет: P2
- Шаги воспроизведения:
  1. POST /api/register с email "not-an-email"
- Фактический результат: 201, пользователь создан
- Ожидаемый результат: 400, сообщение о неверном формате
- Статус: Исправлен (добавлена проверка `'@' not in email or '.' not in email.split('@')[-1]` в routes/auth.py)

## BUG-03. [Minor] SQLite в тестах не принимал event_date строкой
- Серьёзность: Minor
- Приоритет: P3
- Шаги воспроизведения:
  1. Запустить pytest с TESTING=1 (SQLite)
  2. POST /api/events с `"event_date": "2026-11-03T19:00:00"` (строка)
- Фактический результат: TypeError: SQLite DateTime type only accepts Python datetime
- Ожидаемый результат: 201, событие создано
- Статус: Исправлен (добавлена функция `_parse_date()` в routes/events.py)
