import pytest
import allure
from api.user_api import UserApiClient


@allure.suite("Аутентификация пользователей")
class TestUserAuthentication:

    @allure.title("Вход зарегистрированного пользователя — статус 200, возвращаются токены и данные пользователя")
    def test_registered_user_can_login_and_receive_tokens(self, new_user_credentials, auth_payload):
        api_client = UserApiClient()
        
        # Предварительная регистрация пользователя
        api_client.register_new_customer(new_user_credentials)
        
        # Выполнение входа
        response = api_client.authenticate_customer(auth_payload)
        
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        
        response_data = response.json()
        assert response_data.get("success") is True, "success должен быть True"
        assert "accessToken" in response_data, "Отсутствует accessToken"
        assert "refreshToken" in response_data, "Отсутствует refreshToken"
        assert "user" in response_data, "Отсутствует объект user"
        assert response_data["user"].get("email") == new_user_credentials["email"], "Email не совпадает"
        assert response_data["user"].get("name") == new_user_credentials["name"], "Name не совпадает"

    @allure.title("Вход с неверными учётными данными возвращает статус 401 и сообщение об ошибке")
    @pytest.mark.parametrize("invalid_email,invalid_password", [
        ("nonexistent@example.com", "wrongpassword"),
        ("fakeuser@test.ru", "123456"),
        ("", ""),
        ("valid@example.com", ""),
        ("", "somepassword"),
    ])
    def test_login_with_invalid_credentials_returns_401_unauthorized(self, invalid_email, invalid_password):
        api_client = UserApiClient()
        
        wrong_credentials = {
            "email": invalid_email,
            "password": invalid_password
        }
        
        response = api_client.authenticate_customer(wrong_credentials)
        
        assert response.status_code == 401, f"Ожидался 401, получен {response.status_code}"
        
        response_data = response.json()
        assert response_data.get("success") is False, "success должен быть False"
        assert response_data.get("message") == "email or password are incorrect", \
            "Неверное сообщение об ошибке"