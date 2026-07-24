from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.login_input = page.get_by_role("textbox", name="Электронная почта")
        self.password_input = page.get_by_role("textbox", name="Надёжный пароль")
        self.login_button = page.get_by_role("button", name="Войти")
        self.forgot_password_link = page.get_by_role("button", name="Я забыл пароль")

    def navigate(self):
        self.page.goto(
            "https://yozhka.lukit.ru/sign-in",
            timeout=90000  # на загрузку страницы
        )
        self.login_button.wait_for(state="visible", timeout=60000)  # на появление кнопки

    def login(self, username: str, password: str):
        self.login_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def check_successful_login(self, expected_name: str):
        user_menu = self.page.get_by_role("link", name=expected_name)
        expect(user_menu).to_be_visible()

    def check_error_message(self, expected_text: str):
        error_element = self.page.get_by_text(expected_text)
        expect(error_element).to_be_visible()
