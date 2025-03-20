import pytest

@pytest.mark.parametrize("color", [
    ["BLACK"],  # Можно указать один цвет (BLACK)
    ["GREY"],  # Можно указать один цвет (GREY)
    ["BLACK", "GREY"],  # Можно указать оба цвета
    []  # Можно не указывать цвет
])
def test_create_order_with_colors(api_client, color):
    """Проверяет создание заказа с разными вариантами цвета"""
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

@pytest.mark.parametrize("invalid_color", [
    ["RED"],  # Некорректный цвет
    ["YELLOW"],  # Некорректный цвет
    ["BLACK", "RED"],  # Один корректный, один некорректный
    None  # Передача None вместо списка
])
def test_create_order_invalid_color(api_client, invalid_color):
    """Проверяет, что с некорректными цветами заказ не создаётся"""
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
