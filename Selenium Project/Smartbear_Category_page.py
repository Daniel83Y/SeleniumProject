from selenium import webdriver
from selenium.webdriver.common.by import By

class BearStoreCategoryPage:
    def __init__(self, driver: webdriver.Edge):
        """Initialize the BearStoreCategoryPage with a WebDriver instance."""
        self.driver = driver

    def sub_categories(self):
        """Finds and returns a list of sub-category elements available on the category page."""
        try:
            categories = self.driver.find_element(By.CLASS_NAME, "artlist-sub-categories.hide-on-active-filter")
            return categories.find_elements(By.CSS_SELECTOR, 'article > div.art-genericname > a')
        except:
            return None  # Returns None if no sub-categories are found

    def click_category(self, category_name):
        """Clicks on the specified sub-category by matching the provided name (case-insensitive)."""
        categories_list = self.sub_categories()
        if categories_list:
            for category in categories_list:
                if category_name.lower() == category.text.lower():
                    category.click()
                    break  # Stop searching once the correct sub-category is found and clicked

    def product(self):
        """Finds and returns a list of product elements available in the selected sub-category."""
        product_div = self.driver.find_element(By.CSS_SELECTOR, "div.product-list-container > div.artlist.artlist-grid.artlist-4-cols")
        return product_div.find_elements(By.CSS_SELECTOR, "article>h3>a")

    def click_product(self, product_name):
        """Clicks on the specified product by matching the provided product name (case-insensitive)."""
        product_list = self.product()
        for product in product_list:
            if product_name.lower() == product.text.lower():
                product.click()
                break  # Stop searching once the correct product is found and clicked

    def get_category_name(self):
        """Finds and returns the name of the currently selected category."""
        return self.driver.find_element(By.CSS_SELECTOR, '#content-center > div > div.page-title > h1')
