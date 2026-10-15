# Описание API AccessEvent

| Метод | URL | Доступ | Вход (JSON) | Ответы |
|---|---|---|---|---|
| POST | /api/register | все | username, email, password, role | 201 user_id; 400 ошибки; 409 email занят |
| POST | /api/login | все | email, password | 200 token; 401 неверные |
| GET | /api/events | все | — | 200 список |
| POST | /api/events | organizer/admin | title, description, event_date, location, is_inclusive | 201 id; 401 без токена |
| GET | /api/events/<id> | все | — | 200; 404 |
| PUT | /api/events/<id> | organizer/admin | любые поля | 200; 404 |
| DELETE | /api/events/<id> | admin | — | 200; 404 |
| POST | /api/registrations | user (токен) | event_id | 201 id; 404; 409 дубль |
| GET | /api/registrations | user (токен) | — | 200 список |
| GET | /api/profile | user (токен) | — | 200 профиль |

## Примеры

### POST /api/register — запрос
{"username": "anna", "email": "anna@mail.ru", "password": "Passw0rd!", "role": "participant"}

### Ответ 201
{"message": "Пользователь создан", "user_id": 1}

### POST /api/login — запрос
{"email": "anna@mail.ru", "password": "Passw0rd!"}

### Ответ 200
{"token": "eyJhbGci...", "role": "participant", "user_id": 1}

### POST /api/events — запрос
{"title": "Кинопросмотр", "description": "С субтитрами", "event_date": "2026-11-03T19:00:00", "location": "Москва", "is_inclusive": true}

### Ответ 201
{"message": "Мероприятие создано", "id": 5}
