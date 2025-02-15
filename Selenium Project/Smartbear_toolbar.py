from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class BearStoreToolBar:
    def __init__(self,driver:webdriver.Chrome):
        """Initialize the BearStoreToolBar with a WebDriver instance."""
        self.driver = driver

    def toolbar_logo(self):
        """Returns to Smart Bear main page"""
        return self.driver.find_element(By.CLASS_NAME,"brand")

    def toolbar_menu(self):
        """Opens menu in smart bear mainpage"""
        return self.driver.find_element(By.ID,"shopbar-menu")
    def toolbar_menu_click(self):
        self.toolbar_menu().click()
    def toolbar_account_click(self):
        account = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "nav#menubar-my-account > div.dropdown > a")))
        self.driver.execute_script("arguments[0].click();", account)
    def toolbar_logout(self):
        logout_account = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.dropdown-menu.dropdown-menu-right.show > a")))
        self.driver.execute_script("arguments[0].click();", logout_account[-1])

    def toolbar_login(self):
        return self.driver.find_element(By.CSS_SELECTOR,"nav#menubar-my-account > div.dropdown > a")
    def toolbar_login_click(self):
        self.toolbar_login().click()
    def toolbar_account_name(self):
        return self.driver.find_element(By.CSS_SELECTOR, "nav#menubar-my-account > div.dropdown > a > span")

    def toolbar_compare(self):
        return self.driver.find_element(By.CSS_SELECTOR,"shopbar-compare>a")
    def toolbar_compare_click(self):
        self.toolbar_compare().click()

    def toolbar_wishlist(self):
        return self.driver.find_element(By.ID, "shopbar-wishlist")
    def toolbar_wishlist_click(self):
        self.toolbar_wishlist().click()

    def toolbar_cart(self):
        cart = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#shopbar-cart > a.shopbar-button.navbar-toggler"))
        )
        return cart
    def toolbar_cart_click(self):
        cart = self.toolbar_cart()
        self.driver.execute_script("arguments[0].click();", cart)
    def toolbar_logo_click(self):
        """
        Clicks the toolbar logo using JavaScript if a blocking element prevents a normal click.
        """
        logo = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "brand")))
        self.driver.execute_script("arguments[0].click();", logo)

    def toolbar_search(self):
        return self.driver.find_element(By.CSS_SELECTOR,"form > button")
    def toolbar_search_click(self):
        self.toolbar_search().click()

    def toolbar_search_input(self):
        return self.driver.find_element(By.CLASS_NAME,"instasearch-term form-control")

    def toolbar_search_input_fill(self,fill):
        self.toolbar_search_input().clear()
        self.toolbar_search_input().send_keys(fill)


