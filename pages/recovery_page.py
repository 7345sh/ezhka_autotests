from playwright.sync_api import Page, expect


class RecoveryPage:
    def __init__(self, page: Page):
        self.page = page
        # Страница запроса восстановления
        self.email_input = page.get_by_role("textbox", name="Почта, указанная при регистрации")
        self.change_password_button = page.get_by_role("button", name="Изменить пароль")
        self.back_to_login_link = page.get_by_role("button", name="Войти")
        # Страница изменения пароля
        self.new_password_input = page.get_by_role("textbox", name="Пароль")
        self.confirm_password_input = page.get_by_role("textbox", name="Повтори пароль")
        self.submit_button = page.get_by_role("button", name="Подтвердить")
        # Кнопка требований на странице изменения пароля
        self.requirements_button = page.get_by_role("button", name="Требования к паролю")

    def navigate_to_recovery(self):
        forgot_link = self.page.get_by_role("button", name="Я забыл пароль")
        forgot_link.wait_for(state="visible", timeout=30000)
        forgot_link.click()
        self.email_input.wait_for(state="visible", timeout=30000)

    def request_password_reset(self, email: str):
        self.email_input.fill(email)
        self.change_password_button.click()

    def check_success_message(self):
        success_text = self.page.get_by_text("Перейди по ссылке в письме")
        expect(success_text).to_be_visible()

    def check_error_message(self, expected_text: str):
        error_element = self.page.get_by_text(expected_text)
        expect(error_element).to_be_visible()

    def check_empty_field_error(self):
        error_text = self.page.get_by_text("Введи логин в формате " \
        "электронной почты", exact=False)
        expect(error_text).to_be_visible()
