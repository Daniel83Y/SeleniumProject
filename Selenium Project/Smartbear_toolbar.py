from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class BearStoreToolBar:
    def __init__(self, driver: webdriver.Chrome):
        """Initialize the BearStoreToolBar with a WebDriver instance."""
        self.driver = driver

    def toolbar_logo(self):
        """Returns the toolbar logo element, which navigates to the Smart Bear main page."""
        return self.driver.find_element(By.CLASS_NAME, "brand")

    def toolbar_menu(self):
        """Returns the menu button element in the Smart Bear main page."""
        return self.driver.find_element(By.ID, "shopbar-menu")

    def toolbar_menu_click(self):
        """Clicks on the menu button in the toolbar."""
        self.toolbar_menu().click()

    def toolbar_account_click(self):
        """Clicks on the account dropdown in the toolbar."""
        account = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "nav#menubar-my-account > div.dropdown > a"))
        )
        self.driver.execute_script("arguments[0].click();", account)

    def toolbar_logout(self):
        """Finds and clicks the logout option in the account dropdown."""
        logout_account = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.dropdown-menu.dropdown-menu-right.show > a"))
        )
        self.driver.execute_script("arguments[0].click();", logout_account[-1])

    def toolbar_login(self):
        """Returns the login button element in the toolbar."""
        return self.driver.find_element(By.CSS_SELECTOR, "nav#menubar-my-account > div.dropdown > a")

    def toolbar_login_click(self):
        """Clicks the login button in the toolbar."""
        self.toolbar_login().click()

    def toolbar_account_name(self):
        """Returns the element containing the account name displayed in the toolbar."""
        return self.driver.find_element(By.CSS_SELECTOR, "nav#menubar-my-account > div.dropdown > a > span")

    def toolbar_compare(self):
        """Returns the compare button element in the toolbar."""
        return self.driver.find_element(By.CSS_SELECTOR, "shopbar-compare>a")

    def toolbar_compare_click(self):
        """Clicks the compare button in the toolbar."""
        self.toolbar_compare().click()

    def toolbar_wishlist(self):
        """Returns the wishlist button element in the toolbar."""
        return self.driver.find_element(By.ID, "shopbar-wishlist")

    def toolbar_wishlist_click(self):
        """Clicks the wishlist button in the toolbar."""
        self.toolbar_wishlist().click()

    def toolbar_cart(self):
        """Returns the shopping cart button element in the toolbar."""
        cart = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#shopbar-cart > a.shopbar-button.navbar-toggler"))
        )
        return cart

    def toolbar_cart_click(self):
        """Clicks the shopping cart button in the toolbar using JavaScript to avoid overlay issues."""
        cart = self.toolbar_cart()
        self.driver.execute_script("arguments[0].click();", cart)

    def toolbar_logo_click(self):
        """
        Clicks the toolbar logo using JavaScript if a blocking element prevents a normal click.
        Navigates to the homepage.
        """
        logo = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "brand"))
        )
        self.driver.execute_script("arguments[0].click();", logo)

    def toolbar_search(self):
        """Returns the search button element in the toolbar."""
        return self.driver.find_element(By.CSS_SELECTOR, "form > button")

    def toolbar_search_click(self):
        """Clicks the search button in the toolbar."""
        self.toolbar_search().click()

    def toolbar_search_input(self):
        """Returns the search input field element in the toolbar."""
        return self.driver.find_element(By.CLASS_NAME, "instasearch-term form-control")

    def toolbar_search_input_fill(self, fill):
        """Clears the search input field and fills it with the provided text."""
        self.toolbar_search_input().clear()
        self.toolbar_search_input().send_keys(fill)
