import pytest
from pages.recovery_page import RecoveryPage
from pages.login_page import LoginPage
from playwright.sync_api import expect


# Положительные ТК
# Успешный ввод адреса электронной почты для смены пароля
def test_tc_2_1_1_request_reset_valid_email(page, test_user):
    recovery_page = RecoveryPage(page)
    login_page = LoginPage(page)
    login_page.navigate()
    recovery_page.navigate_to_recovery()
    recovery_page.request_password_reset(test_user["email"])
    recovery_page.check_success_message()

# Отрицательные ТК
# Ввод некорректного логина при изменении пароля
def test_tc_2_2_1_request_reset_invalid_email(page):
    recovery_page = RecoveryPage(page)
    login_page = LoginPage(page)
    login_page.navigate()
    recovery_page.navigate_to_recovery()
    recovery_page.request_password_reset("invalid_email")
    recovery_page.check_error_message("Введи логин в формате электронной почты")

# Ввод почтового адреса, отсутствующего в системе, при изменения пароля
def test_tc_2_2_2_request_reset_nonexistent_email(page):
    recovery_page = RecoveryPage(page)
    login_page = LoginPage(page)
    login_page.navigate()
    recovery_page.navigate_to_recovery()
    recovery_page.request_password_reset("nonexistent@gmail.com")
    recovery_page.check_error_message("Такой пользователь не найден")

# Ввод пустого логина при изменении пароля
def test_tc_2_2_3_request_reset_empty_email(page):
    recovery_page = RecoveryPage(page)
    login_page = LoginPage(page)
    login_page.navigate()
    recovery_page.navigate_to_recovery()
    recovery_page.request_password_reset("")
    recovery_page.check_empty_field_error()


