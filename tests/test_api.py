def _register_and_login(client, email, role="organizer"):
    """Вспомогательная функция: создаёт пользователя и возвращает JWT."""
    client.post("/api/register", json={
        "username": email.split("@")[0],
        "email": email,
        "password": "Passw0rd!",
        "role": role,
    })
    resp = client.post("/api/login", json={
        "email": email,
        "password": "Passw0rd!",
    })
    return resp.get_json()["token"]


def test_register_success(client):
    resp = client.post("/api/register", json={
        "username": "anna",
        "email": "anna@mail.ru",
        "password": "Passw0rd!",
        "role": "participant",
    })
    assert resp.status_code == 201
    assert "user_id" in resp.get_json()


def test_register_invalid_email_rejected(client):
    resp = client.post("/api/register", json={
        "username": "bob",
        "email": "not-an-email",
        "password": "Passw0rd!",
        "role": "participant",
    })
    assert resp.status_code == 400


def test_register_duplicate_email_returns_409(client):
    client.post("/api/register", json={
        "username": "dup",
        "email": "dup@mail.ru",
        "password": "Passw0rd!",
        "role": "participant",
    })
    resp = client.post("/api/register", json={
        "username": "dup2",
        "email": "dup@mail.ru",
        "password": "Passw0rd!",
        "role": "participant",
    })
    assert resp.status_code == 409


def test_login_returns_token(client):
    client.post("/api/register", json={
        "username": "org",
        "email": "org@mail.ru",
        "password": "Passw0rd!",
        "role": "organizer",
    })
    resp = client.post("/api/login", json={
        "email": "org@mail.ru",
        "password": "Passw0rd!",
    })
    assert resp.status_code == 200
    assert "token" in resp.get_json()


def test_create_event_requires_token(client):
    resp = client.post("/api/events", json={
        "title": "Лекция",
        "description": "d",
        "event_date": "2026-11-01T12:00:00",
        "location": "Москва",
    })
    assert resp.status_code in (401, 403)


def test_events_list_public(client):
    resp = client.get("/api/events")
    assert resp.status_code == 200


def test_create_event_with_token(client):
    token = _register_and_login(client, "org3@mail.ru", role="organizer")
    headers = {"Authorization": "Bearer " + token}
    resp = client.post("/api/events", json={
        "title": "Тихий кинопросмотр",
        "description": "С субтитрами",
        "event_date": "2026-11-03T19:00:00",
        "location": "Москва",
        "is_inclusive": True,
        "sign_language": True,
        "visual_alerts": True,
    }, headers=headers)
    assert resp.status_code == 201
    assert "id" in resp.get_json()


def test_register_for_event_and_list(client):
    # Arrange: организатор создаёт мероприятие
    org_token = _register_and_login(client, "org4@mail.ru", role="organizer")
    client.post("/api/events", json={
        "title": "Экскурсия",
        "description": "d",
        "event_date": "2026-11-03T12:00:00",
        "location": "СПб",
    }, headers={"Authorization": "Bearer " + org_token})
    events = client.get("/api/events").get_json()
    event_id = events[0]["id"]

    # Act: участник регистрируется на мероприятие
    user_token = _register_and_login(client, "p4@mail.ru", role="participant")
    headers = {"Authorization": "Bearer " + user_token}
    resp = client.post("/api/registrations",
                       json={"event_id": event_id}, headers=headers)
    assert resp.status_code == 201

    # Проверка списка «моих регистраций»
    resp = client.get("/api/registrations", headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["event_id"] == event_id
