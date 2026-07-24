import pytest
import oc
import time
import random
from playwright.sync_api import Page, BrowserContext

# Берёт персональные данные из файла .env
TEST_USER = {
    "email": os.getenv("TEST_USER_EMAIL"),
    "password": os.getenv("TEST_USER_PASSWORD"),
    "full_name": os.getenv("TEST_USER_FULL_NAME")
}

# Возвращает тестовые данные пользователя
@pytest.fixture
def test_user():
    return TEST_USER

# Создаёт новую страницу для каждого теста
@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page
    page.close()

# Генерирует уникальное имя проекта
def unique_name(base="Проект"):
    return f"{base} {int(time.time())}{random.randint(10, 99)}"

# Генерирует уникальный код проекта (4 цифры)
def unique_code(prefix="AT"):
    return f"{prefix}{int(time.time()) % 10000:04d}"
