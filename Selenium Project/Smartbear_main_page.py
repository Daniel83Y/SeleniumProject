from selenium import webdriver
from selenium.webdriver.common.by import By

class BearStoreMainPage:
    def __init__(self, driver: webdriver.Chrome):
        """Initializes the BearStoreMainPage with a WebDriver instance for interacting with the website."""
        self.driver = driver

    def categories(self):
        """Finds and returns a list of category elements available on the BearStore main page."""
        categories_div = self.driver.find_element(By.CLASS_NAME, 'artlist-homepage-categories')
        return categories_div.find_elements(By.CSS_SELECTOR, 'article > div.art-genericname > a')

    def click_category(self, category_name):
        """Clicks on the specified category by matching the provided category name (case-insensitive)."""
        categories_list = self.categories()
        for category in categories_list:
            if category_name.lower() == category.text.lower():
                category.click()
                break  # Stop searching once the correct category is found and clicked

    def featured_products(self):
        """Finds and returns a list of featured product elements displayed on the homepage."""
        featured_prods = self.driver.find_element(By.CSS_SELECTOR, '#artlist-7040135593')
        return featured_prods.find_elements(By.CSS_SELECTOR, 'article > h3')

    def click_featured_product(self, product_name):
        """Clicks on the specified featured product by matching the provided product name (case-insensitive)."""
        featured_prods = self.featured_products()
        for prod in featured_prods:
            if product_name.lower() == prod.text.lower():
                prod.click()
                break  # Stop searching once the correct product is found and clicked
