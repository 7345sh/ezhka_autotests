import pytest
from pages.login_page import LoginPage
from pages.project_page import ProjectPage
from playwright.sync_api import expect
from conftest import unique_name, unique_code


@pytest.fixture
def login_and_navigate(page, test_user):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(test_user["email"], test_user["password"])
    page.get_by_role("link", name=test_user["full_name"]).wait_for(state="visible", timeout=30000)
    project_page = ProjectPage(page)
    project_page.navigate_to_projects_tab()
    return project_page

# Создание проекта
# Положительные ТК
# Создание проекта с валидными данными (упрощённый ТК)
def test_tc_3_1_1_1_create_project_success(page, login_and_navigate):
    project_page = login_and_navigate
    name = unique_name()
    project_page.create_project(name)
    expect(project_page.get_project_link(name)).to_be_visible()
    project_page.delete_project(name)

# Отрицательные ТК
# Создание проекта без названия
def test_tc_3_1_2_1_create_project_with_empty_name(page, login_and_navigate):
    project_page = login_and_navigate
    project_page.open_create_project_modal()
    project_page.project_name_input.fill("")
    expect(project_page.create_button).to_be_disabled()

# Добавление проекта в избранное
# Положительные ТК
# Успешное добавление проекта в избранное
def test_tc_3_2_1_1_add_to_favorites(page, login_and_navigate):
    project_page = login_and_navigate
    name = unique_name()
    project_page.create_project(name)
    project_page.add_to_favorites(name)
    project_page.delete_project(name)

# Успешное удаление проекта из избранного
def test_tc_3_2_1_2_remove_from_favorites(page, login_and_navigate):
    """ТК-3.8 Удаление проекта из избранного."""
    project_page = login_and_navigate
    name = unique_name()
    project_page.create_project(name)
    project_page.add_to_favorites(name)
    project_page.remove_from_favorites(name)
    project_page.delete_project(name)

# Изменение проекта
# Положительные ТК
# Успешное изменение названия
def test_tc_3_3_1_1_rename_project(page, login_and_navigate):
    project_page = login_and_navigate
    name = unique_name()
    new_name = unique_name()
    project_page.create_project(name)
    project_page.rename_project(new_name)
    # название должно обновиться и в меню навигации, и на доске
    expect(project_page.get_project_link(new_name)).to_be_visible(timeout=10000)
    expect(project_page.get_project_link(name)).not_to_be_visible()
    project_page.delete_project(new_name)

# Архивирование проекта
# Положительные ТК
# Успешное архивирование проекта
def test_tc_3_4_1_1_archive_project(page, login_and_navigate):
    project_page = login_and_navigate
    name = unique_name()
    project_page.create_project(name)
    project_page.archive_project(name)
    project_page.restore_project(name)
    project_page.delete_project(name)

# Успешное восстановление проекта
def test_tc_3_4_1_2_restore_project(page, login_and_navigate):
    project_page = login_and_navigate
    name = unique_name()
    project_page.create_project(name)
    project_page.archive_project(name)
    project_page.restore_project(name)
    project_page.delete_project(name)

# Положительные ТК
# Архивирование проекта с неверным кодом проекта
def test_tc_3_4_2_1_archive_with_wrong_code(page, login_and_navigate):
    project_page = login_and_navigate
    name = unique_name()
    project_page.create_project(name)
    project_page.open_project(name)
    project_page.open_board_menu(name)
    project_page.page.get_by_text("Архивировать").click()
    confirm_input = project_page.page.get_by_role("textbox")
    confirm_input.fill("WRONG")
    expect(project_page.page.get_by_role("button", name="Архивировать")).to_be_disabled()

# Удаление проекта
# Положительные ТК
# Успешное удаление проекта
def test_tc_3_5_1_1_delete_project(page, login_and_navigate):
    project_page = login_and_navigate
    name = unique_name()
    project_page.create_project(name)
    project_page.delete_project(name)