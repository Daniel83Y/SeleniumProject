from selenium import webdriver
from selenium.webdriver.common.by import By
class BearStoreToolBar:
    def __init__(self,driver:webdriver.Chrome):
        """Initialize the BearStoreToolBar with a WebDriver instance."""
        self.driver = driver

    def toolbar_logo(self):
        """Returns to Smart Bear main page"""
        return self.driver.find_element(By.CLASS_NAME,"brand")
    def toolbar_logo_click(self):
        self.toolbar_logo().click()

    def toolbar_menu(self):
        """Opens menu in smart bear mainpage"""
        return self.driver.find_element(By.ID,"shopbar-menu")
    def toolbar_menu_click(self):
        self.toolbar_menu().click()

    def toolbar_login(self):
        return self.driver.find_element(By.ID,"shopbar-user")
    def toolbar_login_click(self):
        self.toolbar_login().click()

    def toolbar_compare(self):
        return self.driver.find_element(By.ID,"shopbar-user")
    def toolbar_compare_click(self):
        self.toolbar_compare().click()

    def toolbar_wishlist(self):
        return self.driver.find_element(By.ID, "shopbar-wishlist")
    def toolbar_wishlist_click(self):
        self.toolbar_wishlist().click()

    def toolbar_cart(self):
        return self.driver.find_element(By.ID, "shopbar-cart")

    def toolbar_cart_click(self):
        self.toolbar_cart().click()

    def toolbar_search(self):
        return self.driver.find_element(By.CSS_SELECTOR,"form > button")
    def toolbar_search_click(self):
        self.toolbar_search().click()

    def toolbar_search_input(self):
        return self.driver.find_element(By.CLASS_NAME,"instasearch-term form-control")

    def toolbar_search_input_fill(self,fill):
        self.toolbar_search_input().clear()
        self.toolbar_search_input().send_keys(fill)

