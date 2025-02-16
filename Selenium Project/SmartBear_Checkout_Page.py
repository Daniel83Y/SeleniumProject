from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BearStoreCheckoutPage:
    def __init__(self, driver: webdriver.Edge):
        """Initialize the BearStoreCheckoutPage with a WebDriver instance."""
        self.driver = driver

    def billing_address(self):
        """Finds and returns the billing address selection button."""
        address = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.address-item > button'))
        )
        return address

    def click_billing_address(self):
        """Clicks the billing address selection button using JavaScript."""
        address = self.billing_address()
        self.driver.execute_script('arguments[0].click();', address)

    def shipping_address(self):
        """Finds and returns the shipping address selection button."""
        address = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.address-item > button'))
        )
        return address

    def click_shipping_address(self):
        """Clicks the shipping address selection button using JavaScript."""
        address = self.shipping_address()
        self.driver.execute_script('arguments[0].click();', address)

    def confirm_shipping_method(self):
        """Finds and clicks the button to confirm the selected shipping method."""
        confirm = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.buttons>button.shipping-method-next-step-button'))
        )
        self.driver.execute_script('arguments[0].click();', confirm)

    def confirm_payment_method(self):
        """Finds and clicks the button to confirm the selected payment method."""
        confirm = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div>button.payment-method-next-step-button'))
        )
        self.driver.execute_script('arguments[0].click();', confirm)

    def agree_to_terms(self):
        """Finds and clicks the checkbox to agree to the terms and conditions before checkout."""
        agree = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input#termsofservice'))
        )
        self.driver.execute_script('arguments[0].click();', agree)

    def confirm_checkout(self):
        """Finds and clicks the final checkout confirmation button to place the order."""
        confirm = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn-buy'))
        )
        self.driver.execute_script('arguments[0].click();', confirm)

    def get_order_number(self):
        """Finds and returns the order number element after checkout."""
        order_number = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p > a > strong'))
        )
        return order_number

    def go_to_order_details(self):
        """Finds and clicks the button to navigate to the order details page."""
        order_details = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.btn.btn-warning'))
        )
        self.driver.execute_script('arguments[0].click();', order_details)

    def get_completed_order_number(self):
        """Finds and returns the completed order number text after order placement."""
        completed_order_number = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.page-title.mb-3.col > h1 > small > small'))
        )
        return completed_order_number.text
