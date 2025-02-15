from selenium import webdriver
from selenium.webdriver.common.by import By
from random import choice
class BearStoreProductPage:
    def __init__(self,driver:webdriver.Edge):
        """Initialize the BearStoreMainPage with a WebDriver instance."""
        self.driver = driver

    def breadcrumbs(self):
        """Returns the breadcrumbs trail"""
        return self.driver.find_element(By.CLASS_NAME,'breadcrumb-container')

    def current_active_crumb(self):
        return self.breadcrumbs().find_element(By.CLASS_NAME,'active')

    def inactive_breadcrumbs(self):
        return self.breadcrumbs().find_elements(By.CSS_SELECTOR,'ol > li.breadcrumb-item > a')

    def breadcrumbs_nav(self,content):
        crumbs_list = self.inactive_breadcrumbs()
        for crumb in crumbs_list:
            if crumb.text == content:
                crumb.click()

    def get_product_name(self):
        """Returns the product name"""
        return self.driver.find_element(By.CSS_SELECTOR, 'div.page-title > h1')

    def get_product_price(self):
        """Returns the product price"""
        return self.driver.find_element(By.CSS_SELECTOR,'div.pd-price > span')
    def add_to_cart(self):
        self.driver.find_element(By.CLASS_NAME,"btn-add-to-cart").click()
    def quantity(self):
        return self.driver.find_element(By.CSS_SELECTOR,'input.form-control.form-control-lg')
    def change_quantity(self,random_quantity):
        self.quantity().clear()
        self.quantity().send_keys(random_quantity)

    def choose_color(self):
        choice(self.driver.find_elements(By.CSS_SELECTOR, '#choice-boxes-13 > ul')).click()