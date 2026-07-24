import pytest
from pages.login_page import LoginPage


# Положительные ТК
# Успешная авторизация с корректными данными
def test_tc_1_1_1_successful_login(page, test_user):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(test_user["email"], test_user["password"])
    login_page.check_successful_login(test_user["full_name"])

# Отрицательные ТК
# Авторизация с неверным логином
def test_tc_1_2_1_invalid_login(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("nonexistent@gmail.com", "21052006Zandem?")
    login_page.check_error_message("Логин или пароль указаны неверно")

# Авторизация с пустым полем «Логин»
def test_tc_1_2_2_empty_login(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login_button.click()
    login_page.check_error_message("Введи логин в формате электронной почты")

# Авторизация с неверным паролем
def test_tc_1_2_3_invalid_password(page, test_user):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(test_user["email"], "Wrong_password123")
    login_page.check_error_message("Логин или пароль указаны неверно")

# Авторизация с некорректным паролем
def test_tc_1_2_4_password_not_meet_requirements(page, test_user):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(test_user["email"], "123")
    login_page.check_error_message("Пароль не подходит")

# Авторизация с пустым полем "Пароль"
def test_tc_1_2_5_empty_password(page, test_user):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login_input.fill(test_user["email"])
    login_page.login_button.click()
    login_page.check_error_message("Обязательное поле")