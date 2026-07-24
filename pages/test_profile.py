import re
import pytest
import os
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from playwright.sync_api import expect


@pytest.fixture
def login_and_open_profile(page, test_user):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(test_user["email"], test_user["password"])
    
    page.wait_for_timeout(5000)
    
    parts = test_user["full_name"].split()
    if len(parts) >= 2:
        search_text = " ".join(parts[1:])
    else:
        search_text = test_user["full_name"]
    page.get_by_role("link").filter(has_text=search_text).wait_for(state="visible", timeout=60000)
    profile_page = ProfilePage(page)
    profile_page.open_profile(test_user["full_name"])
    return profile_page


@pytest.fixture
def disposable_login_and_open_profile(page, disposable_user):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(disposable_user["email"], disposable_user["password"])
    
    # Ожидание успешного входа (появление ссылки с именем пользователя)
    parts = disposable_user["full_name"].split()
    if len(parts) >= 2:
        search_text = " ".join(parts[1:])
    else:
        search_text = disposable_user["full_name"]
    page.get_by_role("link").filter(has_text=search_text).wait_for(state="visible", timeout=60000)
    
    profile_page = ProfilePage(page)
    profile_page.open_profile(disposable_user["full_name"])
    return profile_page

# Редактирование основной информации
# Положительные ТК
# Редактирование основной информации

# Тест-кейс 4.2.1.1 детализирован для лучшей обработки ошибок
def test_tc_4_2_1_1_edit_position(page, login_and_open_profile):
    profile_page = login_and_open_profile
    profile_page.edit_field(1, "Практикант")
    expect(page.get_by_text("Практикант", exact=False)).to_be_visible(timeout=10000)

def test_tc_4_2_1_1_edit_city(page, login_and_open_profile):
    profile_page = login_and_open_profile
    profile_page.edit_field(2, "Тула")
    expect(page.get_by_text("Тула", exact=False)).to_be_visible(timeout=10000)

# Редактирование раздела «Контакты и личное» (сокращённо)
def test_tc_4_2_1_2_edit_phone(page, login_and_open_profile):
    profile_page = login_and_open_profile
    profile_page.edit_field(4, "+79109999999")
    expect(page.get_by_text("+79109999999", exact=False)).to_be_visible(timeout=10000)

# Добавление периода отсутствия
def test_tc_4_2_1_7_set_absence_period(page, login_and_open_profile):
    profile_page = login_and_open_profile
    profile_page.set_absence("1", "31")
    expect(page.get_by_text("Недоступен", exact=False)).to_be_visible(timeout=10000)

# Отрицательные ТК
# Попытка стереть ФИО
def test_tc_4_2_2_1_empty_full_name(page, login_and_open_profile):
    profile_page = login_and_open_profile
    field = profile_page.editable_fields.first
    field.click()
    textbox = page.get_by_role("textbox", name="Заполнить")
    textbox.fill("")
    textbox.press("Enter")
    expect(page.get_by_text("Не удалось обновить данные пользователя", exact=False)).to_be_visible(timeout=10000)
