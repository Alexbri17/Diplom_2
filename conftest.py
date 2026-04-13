import pytest
import allure
from api.user_api import UserApiClient
from api.order_api import OrderApiClient
from data import generate_unique_credentials


@pytest.fixture(scope="function", name="new_user_credentials")
def fixture_new_user_credentials():
    """Фикстура: генерирует уникальные данные для нового пользователя."""
    with allure.step("Генерация уникальных учётных данных пользователя"):
        credentials = generate_unique_credentials()
    return credentials


@pytest.fixture(scope="function", name="auth_payload")
def fixture_auth_payload(new_user_credentials):
    """Фикстура: формирует payload для авторизации из данных пользователя."""
    with allure.step("Подготовка данных для авторизации"):
        auth_payload = {
            "email": new_user_credentials["email"],
            "password": new_user_credentials["password"]
        }
    return auth_payload


@pytest.fixture(scope="function", name="user_api")
def fixture_user_api():
    """Фикстура: предоставляет клиент для работы с API пользователей."""
    with allure.step("Инициализация клиента User API"):
        api_client = UserApiClient()
    return api_client


@pytest.fixture(scope="function", name="order_api")
def fixture_order_api():
    """Фикстура: предоставляет клиент для работы с API заказов."""
    with allure.step("Инициализация клиента Order API"):
        api_client = OrderApiClient()
    return api_client


@pytest.fixture(scope="function", name="access_token")
def fixture_access_token(user_api, new_user_credentials, auth_payload):
    """
    Фикстура: создаёт пользователя, выполняет логин и возвращает токен доступа.
    """
    with allure.step("Регистрация нового пользователя"):
        register_response = user_api.register_new_customer(new_user_credentials)
        
        # Если пользователь уже существует, пробуем просто войти
        if register_response.status_code == 403:
            allure.attach("Пользователь уже существует, пробуем войти", name="Registration skipped")
    
    with allure.step("Авторизация пользователя"):
        login_response = user_api.authenticate_customer(auth_payload)
        
        # Проверяем, что логин успешен
        assert login_response.status_code == 200, \
            f"Логин не удался. Статус: {login_response.status_code}, Тело: {login_response.text}"
        
        response_data = login_response.json()
        raw_token = response_data.get('accessToken')
        
        # Проверяем, что токен присутствует
        assert raw_token is not None, \
            f"accessToken отсутствует в ответе. Тело ответа: {response_data}"
        
        # Извлекаем токен из строки "Bearer <token>"
        if 'Bearer ' in raw_token:
            token = raw_token.split('Bearer ')[1]
        else:
            token = raw_token
            
    with allure.step(f"Получен токен: {token[:15]}..."):
        return token