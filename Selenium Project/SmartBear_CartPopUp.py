from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BearStoreCartPopUp:
    def __init__(self,driver:webdriver.Edge):
        """Initialize the BearStoreCartPopUp with a WebDriver instance."""
        self.driver = driver
    def find_cart_items(self):
        try:
            cart_items = self.driver.find_element(By.CLASS_NAME,"offcanvas-cart-items")
            return cart_items.find_elements(By.CLASS_NAME,"offcanvas-cart-item")
        except:
            return None
    def click_remove_item(self,index):
        self.find_cart_items()[index].find_element(By.CSS_SELECTOR,"a.btn-icon.remove.ajax-cart-link").click()
    def cart_total_items_amount(self):
        try:
            element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#cart-tab > span.badge.badge-pill.label-cart-amount.badge-warning'))
            )
            # Additional wait for text content to be updated
            WebDriverWait(self.driver, 2).until(lambda driver: element.text != '')
            return element.text
        except TimeoutException:
            return '0'  # Returning '0' to indicate the cart is empty
    def cart_product_name(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "div.col.col-data > a")
    def cart_product_price(self):
        return self.driver.find_elements(By.CLASS_NAME,"price.unit-price")
    def cart_product_quantity(self):
        return self.driver.find_elements(By.ID,"item_EnteredQuantity")

    def go_to_cart(self):
        cart = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.btn.btn-success'))
        )
        self.driver.execute_script("arguments[0].click();", cart)

    def find_subtotal(self):

        subtotal_element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".sub-total.price"))  # Ensure selector is correct
        )
        return subtotal_element
    def go_to_checkout(self):
        checkout = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.btn.btn-clear.btn-block.btn-action > span')))
        self.driver.execute_script("arguments[0].click();", checkout)