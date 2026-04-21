import pytest
import allure
from api.user_api import UserApiClient
from api.order_api import OrderApiClient
from helpers import extract_access_token_from_response, generate_unique_credentials


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


@pytest.fixture(scope="function", name="created_user")
def fixture_created_user(user_api):
    """
    Фикстура: создаёт пользователя перед тестом и удаляет после теста.
    Очистка происходит ВСЕГДА (даже при падении теста).
    """
    credentials = generate_unique_credentials()
    access_token = None
    
    with allure.step("Регистрация нового пользователя"):
        register_response = user_api.register_new_customer(credentials)
        
        if register_response.status_code == 200:
            access_token = extract_access_token_from_response(register_response.json())
    
    yield {
        "credentials": credentials,
        "access_token": access_token or "",
        "response": register_response
    }
    
    with allure.step("Удаление пользователя после теста (очистка БД)"):
        if access_token:
            user_api.delete_user(access_token)


@pytest.fixture(scope="function", name="access_token")
def fixture_access_token(created_user):
    """Фикстура: возвращает только access_token созданного пользователя."""
    return created_user["access_token"]


@pytest.fixture(scope="function", name="registered_user")
def fixture_registered_user(created_user):
    """Фикстура: для обратной совместимости (алиас created_user)."""
    return created_user