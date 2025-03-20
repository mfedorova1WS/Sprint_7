import pytest
import requests
import allure
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"


def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def create_courier():
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()
    payload = {"login": login, "password": password, "firstName": first_name}
    response = requests.post(f"{BASE_URL}/courier", json=payload)
    if response.status_code == 201:
        return login, password
    return None, None


def delete_courier(login, password):
    response = requests.post(f"{BASE_URL}/courier/login", json={"login": login, "password": password})
    if response.status_code == 200:
        courier_id = response.json()["id"]
        requests.delete(f"{BASE_URL}/courier/{courier_id}")


@allure.feature("Создание курьера")
class TestCreateCourier:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.login, self.password = create_courier()
        yield
        if self.login and self.password:
            delete_courier(self.login, self.password)

    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_fields(self, missing_field):
        payload = {"login": "test_user", "password": "test_pass", "firstName": "Test"}
        del payload[missing_field]
        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code == 400
        assert "message" in response.json()


@allure.feature("Логин курьера")
class TestLoginCourier:

    def test_login_courier(self):
        login, password = create_courier()
        assert login is not None and password is not None
        payload = {"login": login, "password": password}
        response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        assert response.status_code == 200
        assert "id" in response.json()
        delete_courier(login, password)


@allure.feature("Создание заказа")
class TestCreateOrder:

    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_order(self, color):
        payload = {"firstName": "Иван", "lastName": "Иванов", "address": "Москва", "metroStation": 4,
                   "phone": "+79000000000", "rentTime": 5, "deliveryDate": "2025-03-20", "comment": "Тест",
                   "color": color}
        response = requests.post(f"{BASE_URL}/orders", json=payload)
        assert response.status_code == 201
        assert "track" in response.json()


@allure.feature("Список заказов")
class TestGetOrders:

    def test_get_orders(self):
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 200
        assert "orders" in response.json()


if __name__ == "__main__":
    pytest.main()
