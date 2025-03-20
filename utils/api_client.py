import requests

class ApiClient:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'

    def create_courier(self, data):
        return requests.post(f'{self.BASE_URL}/courier', json=data)  # 🔹 Исправлено

    def login_courier(self, data):
        return requests.post(f'{self.BASE_URL}/courier/login', json=data)

    def create_order(self, data):
        return requests.post(f'{self.BASE_URL}/orders', json=data)

    def get_orders(self):
        return requests.get(f'{self.BASE_URL}/orders')

    def delete_courier(self, courier_id):
        return requests.delete(f'{self.BASE_URL}/courier/{courier_id}')
