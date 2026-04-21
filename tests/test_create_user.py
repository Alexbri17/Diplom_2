import pytest
import allure
import copy
from api.user_api import UserApiClient
from helpers import extract_access_token_from_response


@allure.suite("Регистрация новых пользователей")
class TestUserRegistration:

    @allure.title("Успешная регистрация нового пользователя — статус 200 и токены в ответе")
    def test_register_new_user_returns_200_with_tokens(self, created_user):
        """
        Тест использует фикстуру created_user, которая:
        - создаёт пользователя перед тестом
        - удаляет пользователя после теста (даже при падении)
        """
        response_data = created_user["response"].json()
        
        assert created_user["response"].status_code == 200, f"Ожидался 200, получен {created_user['response'].status_code}"
        assert response_data.get("success") is True, "success должен быть True"
        assert "user" in response_data, "Ответ должен содержать поле 'user'"
        assert "email" in response_data["user"], "Поле 'email' отсутствует в объекте user"
        assert "name" in response_data["user"], "Поле 'name' отсутствует в объекте user"
        assert "accessToken" in response_data, "Отсутствует accessToken"
        assert "refreshToken" in response_data, "Отсутствует refreshToken"

    @allure.title("Повторная регистрация того же пользователя возвращает 403 с сообщением 'User already exists'")
    def test_register_existing_user_returns_403_conflict(self, user_api):
        """
        Здесь нужно создать пользователя, но не удалять до второй попытки.
        Поэтому используем ручное создание и удаление.
        """
        from helpers import generate_unique_credentials
        
        new_user_credentials = generate_unique_credentials()
        
        first_response = user_api.register_new_customer(new_user_credentials)
        first_response_data = first_response.json()
        access_token = extract_access_token_from_response(first_response_data)
        
        response = user_api.register_new_customer(new_user_credentials)
        response_data = response.json()
        
        assert response.status_code == 403, f"Ожидался 403, получен {response.status_code}"
        assert response_data.get("success") is False, "success должен быть False"
        assert response_data.get("message") == "User already exists", "Неверное сообщение об ошибке"
        
        if access_token:
            user_api.delete_user(access_token)

    @allure.title("Регистрация с пропущенным обязательным полем возвращает 403 и сообщение о необходимости полей")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_register_user_without_required_field_returns_403(self, missing_field):
        from helpers import generate_unique_credentials
        
        api_client = UserApiClient()
        new_user_credentials = generate_unique_credentials()
        
        incomplete_data = copy.deepcopy(new_user_credentials)
        del incomplete_data[missing_field]
        
        response = api_client.register_new_customer(incomplete_data)
        response_data = response.json()
        
        assert response.status_code == 403, f"Ожидался 403, получен {response.status_code}"
        assert response_data.get("success") is False, "success должен быть False"
        assert response_data.get("message") == "Email, password and name are required fields", \
            "Неверное сообщение об ошибке"     