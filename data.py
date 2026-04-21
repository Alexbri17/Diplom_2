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