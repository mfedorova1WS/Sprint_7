import pytest

def test_login_courier_success(api_client, new_courier):
    """Курьер может авторизоваться и получает id"""
    response = api_client.login_courier({
        "login": new_courier['login'],  # Используем ключ 'login'
        "password": new_courier['password']  # Используем ключ 'password'
    })
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.json()}"
    assert 'id' in response.json(), f"Response does not contain id: {response.json()}"

@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_login_courier_missing_field(api_client, new_courier, missing_field):
    """Если не передать login или password, система вернёт ошибку"""
    invalid_data = {
        "login": new_courier['login'],  # Используем ключ 'login'
        "password": new_courier['password']  # Используем ключ 'password'
    }
    invalid_data.pop(missing_field)  # Удаляем обязательное поле

    response = api_client.login_courier(invalid_data)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.json()}"
    assert "message" in response.json(), f"Expected error message, got {response.json()}"

@pytest.mark.parametrize("invalid_login, invalid_password", [
    ("wrong_login123456", "correct_password"),
    ("correct_login", "wrong_password123456"),
    ("wrong_login123456", "wrong_password123456")
])
def test_login_courier_invalid_credentials(api_client, new_courier, invalid_login, invalid_password):
    """Система вернёт ошибку, если неправильно указать логин или пароль"""
    valid_login, valid_password = new_courier['login'], new_courier['password']

    # Подставляем либо правильные, либо неправильные данные
    login_data = {
        "login": valid_login if invalid_login == "correct_login" else invalid_login,
        "password": valid_password if invalid_password == "correct_password" else invalid_password
    }

    response = api_client.login_courier(login_data)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.json()}"
    assert "message" in response.json(), f"Expected error message, got {response.json()}"

def test_login_non_existent_courier(api_client):
    """Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку"""
    response = api_client.login_courier({
        "login": "nonexistent_user",
        "password": "nonexistent_password"
    })
    assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.json()}"
    assert "message" in response.json(), f"Expected error message, got {response.json()}"
