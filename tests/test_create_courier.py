import pytest

def test_create_courier_success(api_client, valid_courier_data):
    """Курьера можно создать"""
    response = api_client.create_courier(valid_courier_data)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.json()}"
    assert response.json() == {"ok": True}, f"Unexpected response: {response.json()}"

def test_create_duplicate_courier(api_client, new_courier):
    """Нельзя создать двух одинаковых курьеров"""
    response = api_client.create_courier(new_courier)
    assert response.status_code == 409, f"Expected 409, got {response.status_code}: {response.json()}"

@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_create_courier_missing_field(api_client, valid_courier_data, missing_field):
    """Если одного из обязательных полей нет, запрос возвращает 400"""
    invalid_data = valid_courier_data.copy()
    invalid_data.pop(missing_field)

    response = api_client.create_courier(invalid_data)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.json()}"
    assert "message" in response.json(), f"Expected error message, got {response.json()}"


def test_create_courier_conflict(api_client, valid_courier_data):
    """Если создать пользователя с логином, который уже есть, возвращается ошибка"""
    login, password, first_name = valid_courier_data

    api_client.create_courier({
        "login": login,
        "password": password,
        "firstName": first_name
    })

    response = api_client.create_courier({
        "login": login,
        "password": "another_password",
        "firstName": "AnotherName"
    })

    assert response.status_code == 409, f"Expected 409, got {response.status_code}: {response.json()}"
    assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

@pytest.mark.parametrize("invalid_data", [
    {},
    {"login": "", "password": "", "firstName": ""},
    {"password": "valid_pass", "firstName": "ValidName"},
    {"login": "valid_login", "firstName": "ValidName"}
])
def test_create_courier_invalid_request(api_client, invalid_data):
    """Если отправить некорректные данные, запрос возвращает ошибку 400"""
    response = api_client.create_courier(invalid_data)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.json()}"
    assert "message" in response.json(), f"Expected error message, got {response.json()}"