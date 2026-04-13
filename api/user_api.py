import requests
import allure
from url import Url


class UserApiClient:
    """
    Клиент для взаимодействия с API пользователей Stellar Burgers.
    Позволяет регистрировать новых пользователей и выполнять авторизацию.
    """

    def __init__(self):
        self.base_url = Url.BASE_URL
        self.register_endpoint = Url.USER_CREATE
        self.login_endpoint = Url.USER_LOGIN

    @allure.step("Регистрация нового пользователя")
    def register_new_customer(self, account_data: dict) -> requests.Response:
        """
        Создаёт (регистрирует) нового пользователя.
        
        Args:
            account_data: Словарь с полями email, password, name
        
        Returns:
            Response объект с ответом сервера
        """
        response = requests.post(
            self.register_endpoint,
            json=account_data
        )
        return response

    @allure.step("Авторизация пользователя в системе")
    def authenticate_customer(self, credentials: dict) -> requests.Response:
        """
        Выполняет вход пользователя в систему.
        
        Args:
            credentials: Словарь с полями email и password
        
        Returns:
            Response объект с ответом сервера (содержит accessToken, refreshToken)
        """
        response = requests.post(
            self.login_endpoint,
            json=credentials
        )
        return response