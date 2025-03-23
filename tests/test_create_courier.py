import allure
import pytest


@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера, используя валидные данные")
    def test_create_courier_success(self, api_client, valid_courier_data):
        response = api_client.create_courier(valid_courier_data)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.json()}"
        assert response.json() == {"ok": True}, f"Unexpected response: {response.json()}"

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, api_client, new_courier):
        response = api_client.create_courier(new_courier)
        assert response.status_code == 409, f"Expected 409, got {response.status_code}: {response.json()}"
        response_json = response.json()
        assert "message" in response_json, f"No error message in response: {response_json}"
        assert response_json["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title("Нельзя создать курьера, если переданы не все обязательные параметры")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, api_client, valid_courier_data, missing_field):
        invalid_data = valid_courier_data.copy()
        invalid_data.pop(missing_field)
        response = api_client.create_courier(invalid_data)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.json()}"
        response_json = response.json()
        assert "message" in response_json, f"No error message in response: {response_json}"
        assert response_json["message"] == f"Недостаточно данных для создания учетной записи"


    @allure.title("Нельзя создать курьера с существующим логином")
    def test_create_courier_conflict(self, api_client, valid_courier_data):
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

    @allure.title("Нельзя создать курьера, если отправить невалидные данные")
    @pytest.mark.parametrize("invalid_data", [
        {},
        {"login": "", "password": "", "firstName": ""},
        {"password": "valid_pass", "firstName": "ValidName"},
        {"login": "valid_login", "firstName": "ValidName"}
    ])


    def test_create_courier_invalid_request(self, api_client, invalid_data):
        response = api_client.create_courier(invalid_data)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.json()}"
        response_json = response.json()
        assert "message" in response_json, f"No error message in response: {response_json}"
        assert response_json["message"] == "Недостаточно данных для создания учетной записи"
