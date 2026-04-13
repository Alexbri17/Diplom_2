import pytest
import allure
import copy
from api.user_api import UserApiClient


@allure.suite("Регистрация новых пользователей")
class TestUserRegistration:

    @allure.title("Успешная регистрация нового пользователя — статус 200 и токены в ответе")
    def test_register_new_user_returns_200_with_tokens(self, new_user_credentials):
        api_client = UserApiClient()
        response = api_client.register_new_customer(new_user_credentials)
        
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        
        response_data = response.json()
        assert response_data.get("success") is True, "success должен быть True"
        assert "user" in response_data, "Ответ должен содержать поле 'user'"
        assert "email" in response_data["user"], "Поле 'email' отсутствует в объекте user"
        assert "name" in response_data["user"], "Поле 'name' отсутствует в объекте user"
        assert "accessToken" in response_data, "Отсутствует accessToken"
        assert "refreshToken" in response_data, "Отсутствует refreshToken"

    @allure.title("Повторная регистрация того же пользователя возвращает 403 с сообщением 'User already exists'")
    def test_register_existing_user_returns_403_conflict(self, new_user_credentials):
        api_client = UserApiClient()
        
        # Первая регистрация — успешна
        api_client.register_new_customer(new_user_credentials)
        
        # Вторая попытка с теми же данными — должна упасть
        response = api_client.register_new_customer(new_user_credentials)
        response_data = response.json()
        
        assert response.status_code == 403, f"Ожидался 403, получен {response.status_code}"
        assert response_data.get("success") is False, "success должен быть False"
        assert response_data.get("message") == "User already exists", "Неверное сообщение об ошибке"

    @allure.title("Регистрация с пропущенным обязательным полем возвращает 403 и сообщение о необходимости полей")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_register_user_without_required_field_returns_403(self, new_user_credentials, missing_field):
        api_client = UserApiClient()
        
        incomplete_data = copy.deepcopy(new_user_credentials)
        del incomplete_data[missing_field]
        
        response = api_client.register_new_customer(incomplete_data)
        response_data = response.json()
        
        assert response.status_code == 403, f"Ожидался 403, получен {response.status_code}"
        assert response_data.get("success") is False, "success должен быть False"
        assert response_data.get("message") == "Email, password and name are required fields", \
            "Неверное сообщение об ошибке"