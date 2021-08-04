# Некоторые локаторы привязаны к языкозависимому содержимому,
# проверка на язык не выполняется,
# не реализованна проверка на нескольких языках.

# Найденные ошибки:
# #1
# Статус: Ultra Low
# Локация: https://reports.netpeak.net/login
# Место: форма логина, поле логин
# Описание: В теге label аттрибут for имеет значение password, вместо login
# есть
# <label for="password" class="ng-binding md-required">Login</label>
# должно быть
# <label for="login" class="ng-binding md-required">Login</label>
# Влияние: Усложняет автоматизированное тестирование и привязку через локатор
# при смене языка нужно будет реализовывать подстановку локатора
# на нужном языке


import pytest
# pytest plugins
# import pytest_check as check

# import time
# import requests


from selenium import webdriver
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.color import Color

from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import NoSuchElementException

DRIVER = None
WINDOW_SIZE = (1024, 786)
DEF_TIME = 5


@pytest.fixture(scope="module", autouse=True)
def init_driver_0():
    global DRIVER

    DRIVER = webdriver.Firefox(
       executable_path='../selenium/geckodriver-v0.29.1')

    DRIVER.set_window_size(*WINDOW_SIZE)
    DRIVER.set_window_position(600-(WINDOW_SIZE[0]/2), 0)

    yield
    DRIVER.quit()


def get(url, anim=False):
    DRIVER.get(url)
    if not anim:
        DRIVER.execute_script('''
            let style = document.createElement('style');
            style.innerHTML = `
                body *,
                body * :after,
                body * :before {
                animation: none !important;
                transition: none !important;
                }
            `;
            document.head.appendChild(style);
            ''')


class DropDownMenuButton():
    def click(self, locator):
        WebDriverWait(DRIVER, DEF_TIME) \
            .until(EC.element_to_be_clickable(locator)) \
            .click()
        return self

    def menu_el_click(self, locator):
        WebDriverWait(DRIVER, DEF_TIME) \
            .until(EC.element_to_be_clickable(locator)) \
            .click()


class Button():
    def click(self, locator):
        WebDriverWait(DRIVER, DEF_TIME) \
            .until(EC.element_to_be_clickable(locator)) \
            .click()

    def is_activ(self, locator):
        elm = WebDriverWait(DRIVER, DEF_TIME) \
            .until(EC.visibility_of_element_located(locator))
        return elm.is_enabled()


class Field():
    def inputt(self, locator, inpt):
        elm = WebDriverWait(DRIVER, DEF_TIME) \
            .until(EC.element_to_be_clickable(locator))
        ActionChains(DRIVER).send_keys_to_element(elm, inpt).perform()

    def color_border(self, locator, color):
        elm = WebDriverWait(DRIVER, DEF_TIME) \
            .until(EC.element_to_be_clickable(locator))
        return elm.value_of_css_property('border-bottom-color') == color

    def color_label(self, locator, color):
        elm = WebDriverWait(DRIVER, DEF_TIME) \
            .until(EC.element_to_be_clickable(locator))
        return elm.value_of_css_property('color') == color


class CheckBox():
    def check_attr(self, locator):
        elm = WebDriverWait(DRIVER, DEF_TIME) \
            .until(EC.element_to_be_clickable(locator))
        if elm.get_attribute('aria-checked') == 'false':
            elm.click()
        return True


class PopUpMessage():
    def check_msg(self, locator, msg):
        elm = WebDriverWait(DRIVER, DEF_TIME) \
            .until(EC.visibility_of_element_located(locator))
        return elm.text == msg


class Header():
    about_us = DropDownMenuButton()
    about_us.locator = (By.XPATH, '//li[contains(., "О нас")]')
    about_us.team = (
        By.XPATH,
        '//ul[@data-content="about-us-list"]//a[contains(., "Команда")]')
    pers_acc = Button()
    pers_acc.locator = (
        By.XPATH,
        '//div[contains(@class, "header")]//a[contains(., "Личный кабинет")]')


class PageTeam():
    become_part_team = Button()
    become_part_team.locator = (
        By.XPATH,
        '//a[contains(., "Стать частью команды")]')


class PageJob():
    want_job = Button()
    want_job.locator = (
        By.XPATH, '//a[contains(., "Я хочу работать в Netpeak")]')


class PersAccountLogin():
    field_login = Field()
    field_login.locator = (
        By.XPATH, '//input[@id="login"]')
    field_login.label = (
        By.XPATH, '//label[@for="password" and contains(., "Login")]')

    field_password = Field()
    field_password.locator = (
        By.XPATH, '//input[@id="password"]')
    field_password.label = (
        By.XPATH, '//label[@for="password" and contains(., "Password")]')

    login = Button()
    login.locator = (
        By.XPATH, '//button[contains(@class, "enter")]')

    check_allow = CheckBox()
    check_allow.locator = (
        By.XPATH, '//md-checkbox[@aria-label="gdpr"]')

    error_message = PopUpMessage()
    error_message.locator = (
        By.XPATH, '//div[contains(@class, "md-toast-content")]')


class TestCase1():
    def test_tz_1(self):
        # не особо нужно, в задании нет но пусть будет
        DRIVER.set_page_load_timeout(10)
        try:
            get("https://netpeak.ua/")
        except TimeoutException:
            assert False, 'Превышено время загрузки страницы'

    def test_tz_2(self):
        header = Header()
        header.about_us \
            .click(header.about_us.locator) \
            .menu_el_click(header.about_us.team)

    def test_tz_3(self):
        page_team = PageTeam()
        page_team.become_part_team.click(page_team.become_part_team.locator)
        DRIVER.switch_to.window(DRIVER.window_handles[-1])
        assert WebDriverWait(DRIVER, DEF_TIME) \
            .until(EC.url_contains('https://career.netpeak.group/'),
                   'Адрес страницы не соответствует')
        assert WebDriverWait(DRIVER, DEF_TIME) \
            .until(EC.title_contains('Работа в Netpeak:'),
                   'Заголовок не содержит')

    def test_tz_4(self):
        page_job = PageJob()
        assert WebDriverWait(DRIVER, DEF_TIME) \
            .until(EC.element_to_be_clickable(page_job
                                              .want_job
                                              .locator))

    def test_tz_5(self):
        page_team = Header()
        DRIVER.switch_to.window(DRIVER.window_handles[-1-1])
        page_team.pers_acc.click(page_team.pers_acc.locator)
        DRIVER.switch_to.window(DRIVER.
                                window_handles[
                                    DRIVER
                                    .window_handles
                                    .index(DRIVER
                                           .current_window_handle)+1])
        assert WebDriverWait(DRIVER, DEF_TIME) \
            .until(EC.url_contains('https://reports.netpeak.net/login'),
                   'Адрес страницы не соответствует')
        assert WebDriverWait(DRIVER, DEF_TIME) \
            .until(EC.title_contains('Client Dashboard'),
                   'Заголовок не содержит')

    def test_tz_6_7_8_9_10(self):
        pers_account_login = PersAccountLogin()
        pers_account_login.field_login.inputt(
            pers_account_login
            .field_login
            .locator,
            "qwerty")
        pers_account_login.field_password.inputt(
            pers_account_login
            .field_password
            .locator,
            "qwerty")
    # test_tz_7
        assert not pers_account_login.login.is_activ(
            pers_account_login
            .login
            .locator)
    # test_tz_8
        assert pers_account_login.check_allow.check_attr(
            pers_account_login
            .check_allow
            .locator)
        assert pers_account_login.login.is_activ(
            pers_account_login
            .login
            .locator)
        pers_account_login.login.click(
            pers_account_login
            .login
            .locator)
    # test_tz_9
        assert pers_account_login.error_message.check_msg(
            pers_account_login
            .error_message
            .locator,
            'Wrong login or password')
    # test_tz_10
        assert pers_account_login.field_login.color_label(
            pers_account_login
            .field_login
            .label,
            'rgb(221, 44, 0)')
        assert pers_account_login.field_login.color_border(
            pers_account_login
            .field_login
            .locator,
            'rgb(221, 44, 0)')

        assert pers_account_login.field_password.color_label(
            pers_account_login
            .field_password
            .label,
            'rgb(221, 44, 0)')
        assert pers_account_login.field_password.color_border(
            pers_account_login
            .field_password
            .locator,
            'rgb(221, 44, 0)')


# V 1. Перейти по ссылке на главную страницу сайта
#      Netpeak (https://netpeak.ua/).
# V 2. Нажать на кнопку "О нас" и в выпавшем списке нажать кнопку "Команда".
# V 3. Нажать кнопку "Стать частью команды" и убедится что в новой вкладке
#      открылась страница Работа в Нетпик.
# V 4. Убедится что на странице есть кнопка "Я хочу работать в Netpeak"
#      и на нее можно кликнуть.
# V 5. Вернутся на предыдущую вкладку и нажать кнопку "Личный кабинет".
# V 6. На странице личного кабинета заполнить Логин и Пароль
#      случайными данными.
# V 7. Проверить что кнопка "Войти" не доступна.
# V 8. Отметить чекбокс "Авторизируясь, вы соглашаетесь с Политикой
#      конфиденциальности".
# V 9. Нажать на кнопку войти и проверить наличие нотификации о неправильном
#    логине или пароле.
# V 10. Проверить что Логин и Пароль подсветились красным цветом.
