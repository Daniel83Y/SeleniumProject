from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BearStoreCartPopUp:
    def __init__(self, driver: webdriver.Edge):
        """Initialize the BearStoreCartPopUp with a WebDriver instance."""
        self.driver = driver

    def find_cart_items(self):
        """Finds and returns a list of items currently in the cart pop-up."""
        try:
            cart_items = self.driver.find_element(By.CLASS_NAME, "offcanvas-cart-items")
            return cart_items.find_elements(By.CLASS_NAME, "offcanvas-cart-item")
        except:
            return None  # Returns None if no items are found in the cart

    def click_remove_item(self, index):
        """Clicks the remove button for the cart item at the specified index."""
        self.find_cart_items()[index].find_element(By.CSS_SELECTOR, "a.btn-icon.remove.ajax-cart-link").click()

    def cart_total_items_amount(self):
        """Returns the total number of items in the cart as displayed in the cart icon."""
        try:
            element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#cart-tab > span.badge.badge-pill.label-cart-amount.badge-warning')
                )
            )
            # Wait for the text content to be updated
            WebDriverWait(self.driver, 2).until(lambda driver: element.text != '')
            return element.text
        except TimeoutException:
            return '0'  # Returns '0' if the cart is empty

    def cart_product_name(self):
        """Finds and returns a list of product name elements in the cart pop-up."""
        return self.driver.find_elements(By.CSS_SELECTOR, "div.col.col-data > a")

    def cart_product_price(self):
        """Finds and returns a list of product price elements in the cart pop-up."""
        return self.driver.find_elements(By.CLASS_NAME, "price.unit-price")

    def cart_product_quantity(self):
        """Finds and returns a list of product quantity input elements in the cart pop-up."""
        return self.driver.find_elements(By.ID, "item_EnteredQuantity")

    def go_to_cart(self):
        """Clicks the button to navigate to the full shopping cart page."""
        cart = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.btn.btn-success'))
        )
        self.driver.execute_script("arguments[0].click();", cart)

    def find_subtotal(self):
        """Finds and returns the subtotal price element displayed in the cart pop-up."""
        subtotal_element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".sub-total.price"))  # Ensure selector is correct
        )
        return subtotal_element

    def go_to_checkout(self):
        """Clicks the button to proceed to the checkout page from the cart pop-up."""
        checkout = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.btn.btn-clear.btn-block.btn-action > span'))
        )
        self.driver.execute_script("arguments[0].click();", checkout)
