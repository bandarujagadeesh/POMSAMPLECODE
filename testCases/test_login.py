import pytest
from selenium import webdriver
from pageObjects.LoginPage import LoginPage
from utilities.utils import load_test_data
import yaml


@pytest.fixture(scope="module")
def setup():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    with open('config/config.yaml') as file:
        config = yaml.safe_load(file)
    yield driver, config
    driver.quit()


@pytest.mark.parametrize("user_type", ["valid_user", "invalid_user"])
def test_login(setup, user_type):
    driver, config = setup
    test_data = load_test_data('TestData/test_data.json')
    login_page = LoginPage(driver)

    driver.get(config['url'])

    user = test_data[user_type]
    login_page.enter_username(user['username'])
    login_page.enter_password(user['password'])
    login_page.click_login()

    if user_type == "valid_user":
        assert driver.current_url != config['url']
    else:
        assert login_page.get_error_message() == "Epic sadface: Username and password do not match any user in this service"
