import pytest
from utils.api_client import ApiClient
from utils.data_generator import generate_random_string

@pytest.fixture
def api_client():
    return ApiClient()

@pytest.fixture
def valid_courier_data():
    """Генерируем валидные данные курьера, без создания."""
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

@pytest.fixture
def new_courier(api_client, valid_courier_data):
    """Создаем курьера перед тестом и удаляем его после теста"""
    response = api_client.create_courier(valid_courier_data)
    yield valid_courier_data
    # Логинимся, получаем ID и удаляем курьера
    login_response = api_client.login_courier({
        "login": valid_courier_data["login"],
        "password": valid_courier_data["password"]
    })
    if login_response.status_code == 200:
        courier_id = login_response.json()["id"]
        api_client.delete_courier(courier_id)
