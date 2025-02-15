from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait



class BearStoreCartPage:
    def __init__(self,driver:webdriver.Edge):
        """Initialize the BearStoreToolBar with a WebDriver instance."""
        self.driver = driver

    def find_shopping_cart(self):
        cart = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#content-center > div.page.shopping-cart-page')))
        return cart

    def empty_cart(self):
        while True:
            try:
                # Re-locate the remove buttons inside the loop to avoid stale element exception
                remove_btns = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                         'div.cart-row-actions.btn-group-vertical > a.btn-to-danger.btn-sm.btn-icon.ajax-action-link'))
                )
                # If no remove buttons are found, break the loop
                if not remove_btns:
                    break
                # Click the last remove button
                remove_btns[-1].click()
                # Wait for a short period to ensure the element is removed from the DOM
                WebDriverWait(self.driver, 1).until(EC.staleness_of(remove_btns[-1]))
            except (TimeoutException, StaleElementReferenceException):
                # If a timeout or stale element exception occurs, continue the loop to re-locate the elements
                break
    def cart_page_product_name(self):
        prod_names = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'a.cart-item-link')))
        return prod_names
    def cart_page_product_subtotal_price(self):
        subtotal_prod_prices = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,'div.cart-col-subtotal> span.price')))
        return subtotal_prod_prices
    def cart_page_product_price(self):
        prod_prices = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,'div.cart-col-price[data-caption="Price"] > span.price')))
        return prod_prices
    def cart_page_product_quantity(self):
        prod_quantities = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.input-group.bootstrap-touchspin > input')))
        return prod_quantities
    def cart_page_total_price(self):
        total_price = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_element_located((By.CLASS_NAME, 'cart-summary-value')))
        return total_price
    def change_quantity(self,element,quantity):
        element.clear()
        element.send_keys(quantity)

    def cart_summary_total(self):
        sub_total = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'tr.cart-summary-total > td.cart-summary-value > span')))
        return sub_total
    def cart_checkout(self):
        checkout = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.ID,'checkout')))
        self.driver.execute_script("arguments[0].click();", checkout)