import pytest
import allure
from api.user_api import UserApiClient
from api.order_api import OrderApiClient
from helpers import generate_unique_credentials, extract_access_token_from_response


@pytest.fixture(scope="function", name="new_user_credentials")
def fixture_new_user_credentials():
    """Фикстура: генерирует уникальные данные для нового пользователя."""
    with allure.step("Генерация уникальных учётных данных пользователя"):
        credentials = generate_unique_credentials()
    return credentials


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


@pytest.fixture(scope="function", name="registered_user")
def fixture_registered_user(user_api, new_user_credentials):
    """
    Фикстура: создаёт пользователя и возвращает его данные + токен.
    Если пользователь уже существует — удаляет его и создаёт заново.
    После теста пользователь удаляется.
    """
    credentials = new_user_credentials
    access_token = None
    
    with allure.step("Проверка, существует ли пользователь"):
        login_response = user_api.authenticate_customer({
            "email": credentials["email"],
            "password": credentials["password"]
        })
        
        if login_response.status_code == 200:
            with allure.step("Пользователь существует — удаляем его"):
                old_token = extract_access_token_from_response(login_response.json())
                if old_token:
                    user_api.delete_user(old_token)
    
    with allure.step("Регистрация нового пользователя"):
        register_response = user_api.register_new_customer(credentials)
        response_data = register_response.json()
        
        if register_response.status_code == 200:
            access_token = extract_access_token_from_response(response_data)
    
    yield {
        "credentials": credentials,
        "access_token": access_token or "",
        "response": register_response
    }
    
    with allure.step("Удаление пользователя после теста"):
        if access_token:
            user_api.delete_user(access_token)


@pytest.fixture(scope="function", name="access_token")
def fixture_access_token(registered_user):
    """Фикстура: возвращает только access_token зарегистрированного пользователя."""
    return registered_user["access_token"]


@pytest.fixture(scope="function", name="auth_payload")
def fixture_auth_payload(new_user_credentials):
    """
    Фикстура: формирует payload для авторизации из данных пользователя.
    """
    with allure.step("Подготовка данных для авторизации"):
        auth_payload = {
            "email": new_user_credentials["email"],
            "password": new_user_credentials["password"]
        }
    return auth_payload