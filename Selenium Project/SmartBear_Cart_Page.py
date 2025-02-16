from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

class BearStoreCartPage:
    def __init__(self, driver: webdriver.Edge):
        """Initialize the BearStoreCartPage with a WebDriver instance."""
        self.driver = driver

    def find_shopping_cart(self):
        """Finds and returns the shopping cart container element."""
        cart = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#content-center > div.page.shopping-cart-page'))
        )
        return cart

    def empty_cart(self):
        """Removes all products from the shopping cart by repeatedly clicking the remove buttons."""
        while True:
            try:
                # Locate the remove buttons dynamically inside the loop to avoid stale element exceptions
                remove_btns = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                        'div.cart-row-actions.btn-group-vertical > a.btn-to-danger.btn-sm.btn-icon.ajax-action-link'))
                )
                # If no remove buttons are found, break the loop
                if not remove_btns:
                    break
                # Click the last remove button in the list
                remove_btns[-1].click()
                # Wait for the element to be removed from the DOM
                WebDriverWait(self.driver, 1).until(EC.staleness_of(remove_btns[-1]))
            except (TimeoutException, StaleElementReferenceException):
                # If a timeout or stale element exception occurs, exit the loop
                break

    def cart_page_product_name(self):
        """Finds and returns a list of product name elements in the cart."""
        prod_names = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.cart-item-link'))
        )
        return prod_names

    def cart_page_product_subtotal_price(self):
        """Finds and returns a list of product subtotal price elements in the cart."""
        subtotal_prod_prices = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.cart-col-subtotal > span.price'))
        )
        return subtotal_prod_prices

    def cart_page_product_price(self):
        """Finds and returns a list of product price elements in the cart."""
        prod_prices = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.cart-col-price[data-caption="Price"] > span.price'))
        )
        return prod_prices

    def cart_page_product_quantity(self):
        """Finds and returns a list of quantity input elements for products in the cart."""
        prod_quantities = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.input-group.bootstrap-touchspin > input'))
        )
        return prod_quantities

    def cart_page_total_price(self):
        """Finds and returns the total price element displayed in the cart summary."""
        total_price = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'cart-summary-value'))
        )
        return total_price

    def change_quantity(self, index, quantity):
        """Changes the quantity of a product in the shopping cart."""
        quantities = self.cart_page_product_quantity()
        element = quantities[index]
        element.clear()
        element.send_keys(quantity)

    def cart_summary_total(self):
        """Finds and returns the total summary price element in the cart."""
        sub_total = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'tr.cart-summary-total > td.cart-summary-value > span'))
        )
        return sub_total

    def cart_checkout(self):
        """Clicks the checkout button to proceed to the checkout page."""
        checkout = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'checkout'))
        )
        self.driver.execute_script("arguments[0].click();", checkout)
