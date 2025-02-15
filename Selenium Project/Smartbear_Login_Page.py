from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
class BearStoreLoginPage:
    def __init__(self,driver:webdriver.Edge):
        """Initialize the BearStoreLogin with a WebDriver instance."""
        self.driver = driver
    def login_input(self):
        login = self.driver.find_element(By.ID,"UsernameOrEmail")
        return login
    def login_input_sendkeys(self,username):
        self.login_input().clear()
        self.login_input().send_keys(username)
    def password_input(self):
        passwords = self.driver.find_element(By.ID,"Password")
        return passwords
    def password_input_sendkeys(self,password):
        self.password_input().clear()
        self.password_input().send_keys(password)
    def log_in_button(self):
        log_in = self.driver.find_element(By.CSS_SELECTOR, "div > button.btn-login")
        self.driver.execute_script("arguments[0].click();",log_in)