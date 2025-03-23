import allure
import pytest


@allure.feature("Логин курьера")
class TestLoginCourier:
    @allure.title("Успешная авторизация зарегистрированного курьера")
    def test_login_courier_success(self, api_client, new_courier):
        response = api_client.login_courier({
            "login": new_courier['login'],  # Используем ключ 'login'
            "password": new_courier['password']  # Используем ключ 'password'
        })

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.json()}"
        assert 'id' in response.json(), f"Response does not contain id: {response.json()}"

    @allure.title("Курьер не сможет авторизоваться в системе, если не передать обязательные параметры")
    @pytest.mark.parametrize("missing_field", ["login", "password"])


    def test_login_courier_missing_field(self, api_client, new_courier, missing_field):
        invalid_data = {
            "login": new_courier['login'],  # Используем ключ 'login'
            "password": new_courier['password']  # Используем ключ 'password'
        }
        invalid_data.pop(missing_field)  # Удаляем обязательное поле

        response = api_client.login_courier(invalid_data)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.json()}"
        response_json = response.json()
        assert "message" in response_json, f"Expected error message, got {response_json}"
        assert response_json["message"] == "Недостаточно данных для входа", f"Unexpected error message: {response_json['message']}"

    @allure.title("Курьер не сможет авторизоваться в системе, если передать невалидные логин/пароль")
    @pytest.mark.parametrize("invalid_login, invalid_password", [
        ("wrong_login123456", "correct_password"),
        ("correct_login", "wrong_password123456"),
        ("wrong_login123456", "wrong_password123456")
    ])
    def test_login_courier_invalid_credentials(self, api_client, new_courier, invalid_login, invalid_password):
        valid_login, valid_password = new_courier['login'], new_courier['password']

        # Подставляем либо правильные, либо неправильные данные
        login_data = {
            "login": valid_login if invalid_login == "correct_login" else invalid_login,
            "password": valid_password if invalid_password == "correct_password" else invalid_password
    }

        response = api_client.login_courier(login_data)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.json()}"
        response_json = response.json()
        assert "message" in response_json, f"Expected error message, got {response_json}"
        assert response_json["message"] == "Учетная запись не найдена", f"Unexpected error message: {response_json['message']}"


    @allure.title("Нельзя авторизоваться под незарегистрованным курьером")
    def test_login_non_existent_courier(self, api_client):
        response = api_client.login_courier({
            "login": "nonexistent_user",
            "password": "nonexistent_password"
        })
        assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.json()}"
        response_json = response.json()
        assert "message" in response_json, f"Expected error message, got {response_json}"
        assert response_json["message"] == "Учетная запись не найдена", f"Unexpected error message: {response_json['message']}"
