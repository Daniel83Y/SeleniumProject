from selenium import webdriver
from selenium.webdriver.common.by import By
class BearStoreMainPage:
    def __init__(self,driver:webdriver.Chrome):
        """Initialize the BearStoreMainPage with a WebDriver instance."""
        self.driver = driver

    def categories(self):
        """Returns a list of the categories in the BearStoreMainPage."""
        categories_div = self.driver.find_element(By.CLASS_NAME,'artlist-homepage-categories')
        return categories_div.find_elements(By.CSS_SELECTOR,'article > div.art-genericname > a')

    def click_category(self,category_name):
        """Returns the chosen category of the BearStoreMainPage."""
        categories_list = self.categories()
        for category in categories_list:
            if category_name.lower() == category.text.lower():
                category.click()
                break

    def featured_products(self):
        featured_prods = self.driver.find_element(By.CSS_SELECTOR,'#artlist-7040135593')
        return featured_prods.find_elements(By.CSS_SELECTOR,'article > h3')

    def click_featured_product(self, product_name):
        """Returns the chosen product of the BearStoreMainPage."""
        featured_prods = self.featured_products()
        for prod in featured_prods:
            if product_name.lower() == prod.text.lower():
                prod.click()
                break
