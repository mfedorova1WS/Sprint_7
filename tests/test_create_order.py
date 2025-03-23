import allure
import pytest


@allure.feature("Создание заказа")
class TestCreateOrder:
    @allure.title("Заказ успешно создан, если использовать допустимые варианты цвета ")
    @pytest.mark.parametrize("color", [
        ["BLACK"],  # Можно указать один цвет (BLACK)
        ["GREY"],  # Можно указать один цвет (GREY)
        ["BLACK", "GREY"],  # Можно указать оба цвета
        []  # Можно не указывать цвет
    ])
    def test_create_order_with_colors(self, api_client, color):
        response = api_client.create_order({
            "firstName": "Naruto",
            "lastName": "Uzumaki",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": color
        })
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.json()}"
        assert 'track' in response.json(), f"Response does not contain 'track': {response.json()}"

    @allure.title("Нельзя создать заказ, если использовать недопустимые варианты цвета")
    @pytest.mark.parametrize("invalid_color", [
        ["RED"],  # Некорректный цвет
        ["YELLOW"],  # Некорректный цвет
        ["BLACK", "RED"],  # Один корректный, один некорректный
        None  # Передача None вместо списка
    ])
    def test_create_order_invalid_color(self, api_client, invalid_color):
        response = api_client.create_order({
            "firstName": "Naruto",
            "lastName": "Uzumaki",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": invalid_color
        })
        assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.json()}"
        assert "message" in response.json(), f"Expected error message, got {response.json()}"
