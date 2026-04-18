import random
import string
from faker import Faker


def generate_random_string(length: int = 10) -> str:
    """Генерирует случайную строку из латинских букв нижнего регистра."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_unique_credentials(length: int = 10) -> dict:
    """Генерирует уникальные учётные данные для нового пользователя."""
    fake = Faker()
    return {
        "email": fake.email(),
        "password": generate_random_string(length),
        "name": generate_random_string(length)
    }


def extract_access_token_from_response(response_json: dict) -> str:
    """Извлекает accessToken из ответа API."""
    raw_token = response_json.get('accessToken', '')
    if 'Bearer ' in raw_token:
        return raw_token.split('Bearer ')[1]
    return raw_token


def extract_refresh_token_from_response(response_json: dict) -> str:
    """Извлекает refreshToken из ответа API."""
    return response_json.get('refreshToken', '')