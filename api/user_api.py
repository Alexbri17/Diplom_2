import requests
import allure
from url import Url


class UserApiClient:
    """
    Клиент для взаимодействия с API пользователей Stellar Burgers.
    Позволяет регистрировать новых пользователей, выполнять авторизацию и удалять.
    """

    def __init__(self):
        self.base_url = Url.BASE_URL
        self.register_endpoint = Url.USER_CREATE
        self.login_endpoint = Url.USER_LOGIN
        self.user_endpoint = Url.USER_CREATE

    @allure.step("Регистрация нового пользователя")
    def register_new_customer(self, account_data: dict) -> requests.Response:
        """Создаёт (регистрирует) нового пользователя."""
        response = requests.post(
            self.register_endpoint,
            json=account_data
        )
        return response

    @allure.step("Авторизация пользователя в системе")
    def authenticate_customer(self, credentials: dict) -> requests.Response:
        """Выполняет вход пользователя в систему."""
        response = requests.post(
            self.login_endpoint,
            json=credentials
        )
        return response

    @allure.step("Удаление пользователя")
    def delete_user(self, access_token: str) -> requests.Response:
        """Удаляет пользователя по токену."""
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.delete(
            self.user_endpoint,
            headers=headers
        )
        return response