from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class BearStoreCheckoutPage:
    def __init__(self,driver:webdriver.Edge):
        """Initialize the BearStoreCheckout with a WebDriver instance."""
        self.driver = driver

    def billing_address(self):
        address = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.address-item > button')))
        return address

    def click_billing_address(self):
        address = self.billing_address()
        self.driver.execute_script('arguments[0].click();', address)

    def shipping_address(self):
        address = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.address-item > button')))
        return address

    def click_shipping_address(self):
        address = self.shipping_address()
        self.driver.execute_script('arguments[0].click();', address)

    def confirm_shipping_method(self):
        confirm = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.buttons>button.shipping-method-next-step-button')))
        self.driver.execute_script('arguments[0].click();', confirm)

    def confirm_payment_method(self):
        confirm = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div>button.payment-method-next-step-button')))

        self.driver.execute_script('arguments[0].click();', confirm)

    def agree_to_terms(self):
        agree = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input#termsofservice'))
        )
        self.driver.execute_script('arguments[0].click();', agree)

    def confirm_checkout(self):
        confirm = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn-buy'))
        )
        self.driver.execute_script('arguments[0].click();', confirm)

    def get_order_number(self):
        order_number = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p > a > strong'))
        )
        return order_number

    def go_to_order_details(self):
        order_details = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.btn.btn-warning'))
        )
        self.driver.execute_script('arguments[0].click();', order_details)

    def get_completed_order_number(self):
        completed_order_number = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.page-title.mb-3.col > h1 > small > small'))
        )
        return completed_order_number.text