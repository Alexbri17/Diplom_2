import random
import string
from faker import Faker

# ========== Вспомогательные функции ==========

def generate_random_string(length: int = 10) -> str:
    """Генерирует случайную строку из латинских букв нижнего регистра."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_unique_credentials(length: int = 10) -> dict:
    """
    Генерирует уникальные учётные данные для нового пользователя.
    Возвращает словарь с полями: email, password, name.
    """
    fake = Faker()
    
    return {
        "email": fake.email(),
        "password": generate_random_string(length),
        "name": generate_random_string(length)
    }


# ========== Тестовые данные для ингредиентов ==========

# Корректные ID ингредиентов (существуют в системе)
VALID_INGREDIENT_IDS = {
    "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
}

# Некорректный ID ингредиента (не существует в системе)
INVALID_INGREDIENT_IDS = {
    "ingredients": ["invalid_ingredient_id"]
}

# Пустой список ингредиентов (для проверки создания заказа без ингредиентов)
EMPTY_INGREDIENTS = {
    "ingredients": []
}