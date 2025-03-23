import allure
import requests

class ApiClient:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'

    allure.step("Создание курьера")
    def create_courier(self, data):
        return requests.post(f'{self.BASE_URL}/courier', json=data)  # 🔹 Исправлено

    allure.step("Авторизация курьера")
    def login_courier(self, data):
        return requests.post(f'{self.BASE_URL}/courier/login', json=data)

    allure.step("Создание заказа")
    def create_order(self, data):
        return requests.post(f'{self.BASE_URL}/orders', json=data)

    allure.step("Просмотр всех заказов")
    def get_orders(self):
        return requests.get(f'{self.BASE_URL}/orders')

    allure.step("Удаление курьера")
    def delete_courier(self, courier_id):
        return requests.delete(f'{self.BASE_URL}/courier/{courier_id}')
