import allure

@allure.feature("Список заказов")
class TestGetOrders:
    @allure.title("Успешное получение списка заказов")
    def test_get_orders(self, api_client):
        response = api_client.get_orders()
        assert response.status_code == 200
        assert isinstance(response.json()['orders'], list)