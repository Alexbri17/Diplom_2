import requests
import allure
from url import Url


class OrderApiClient:
    """
    Клиент для взаимодействия с API заказов Stellar Burgers.
    Позволяет создавать заказы как с авторизацией, так и без неё.
    """

    def __init__(self):
        self.base_url = Url.BASE_URL
        self.endpoint = Url.ORDER_CREATE

    @allure.step("Отправка запроса на создание заказа")
    def place_new_order(self, ingredients_payload: dict, authorization_token: str = None) -> requests.Response:
        """
        Создаёт новый заказ.
        
        Args:
            ingredients_payload: Словарь с ключом "ingredients", содержащим список ID ингредиентов
            authorization_token: JWT-токен для авторизованных запросов (опционально)
        
        Returns:
            Response объект с ответом сервера
        """
        request_headers = {}
        
        if authorization_token:
            request_headers['Authorization'] = f'Bearer {authorization_token}'
            allure.attach(f"Token: {authorization_token[:15]}...", name="Authorization Token", attachment_type=allure.attachment_type.TEXT)
        
        allure.attach(str(ingredients_payload), name="Request Payload", attachment_type=allure.attachment_type.JSON)
        
        response = requests.post(self.endpoint, json=ingredients_payload, headers=request_headers)
        
        allure.attach(str(response.status_code), name="Response Status Code", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
        
        return response