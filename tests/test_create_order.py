import pytest
import allure
from data import VALID_INGREDIENT_IDS, INVALID_INGREDIENT_IDS, EMPTY_INGREDIENTS


class TestCreateOrder:

    @allure.title("Создание заказа с ингредиентами авторизованным пользователем")
    def test_authorized_user_can_create_order_with_valid_ingredients(self, order_api, access_token):
        response = order_api.place_new_order(VALID_INGREDIENT_IDS, authorization_token=access_token)
        
        assert response.status_code == 200
        assert response.json().get("success") is True
        assert "order" in response.json()

    @allure.title("Создание заказа с ингредиентами без авторизации")
    def test_unauthorized_user_can_create_order_with_valid_ingredients(self, order_api):
        response = order_api.place_new_order(VALID_INGREDIENT_IDS)
        
        assert response.status_code == 200
        assert response.json().get("success") is True
        assert "order" in response.json()

    @allure.title("Невозможно создать заказ без ингредиентов (авторизованный пользователь)")
    def test_authorized_user_cannot_create_order_without_ingredients(self, order_api, access_token):
        response = order_api.place_new_order(EMPTY_INGREDIENTS, authorization_token=access_token)
        
        assert response.status_code == 400
        assert response.json().get("success") is False
        assert response.json().get("message") == "Ingredient ids must be provided"

    @allure.title("Невозможно создать заказ без ингредиентов (неавторизованный пользователь)")
    def test_unauthorized_user_cannot_create_order_without_ingredients(self, order_api):
        response = order_api.place_new_order(EMPTY_INGREDIENTS)
        
        assert response.status_code == 400
        assert response.json().get("success") is False
        assert response.json().get("message") == "Ingredient ids must be provided"

    @allure.title("Создание заказа с невалидным идентификатором ингредиента возвращает ошибку сервера")
    def test_create_order_with_invalid_ingredient_hash_returns_server_error(self, order_api):
        response = order_api.place_new_order(INVALID_INGREDIENT_IDS)
        
        assert response.status_code == 500