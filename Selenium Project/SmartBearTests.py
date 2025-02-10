from unittest import TestCase
from selenium import webdriver
from Smartbear_main_page import BearStoreMainPage
from Smartbear_toolbar import BearStoreToolBar
from Smartbear_Category_page import BearStoreCategoryPage
from SmartBear_Product_Page import BearStoreProductPage
from random import choice, randint
from time import sleep
import logging

# Configure logging for test information
logging.basicConfig(level=logging.INFO)

class SmartBearTest(TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Initialize the Chrome browser
        self.driver = webdriver.Chrome()
        # Navigate to the BearStore test site
        self.driver.get("https://bearstore-testsite.smartbear.com")
        # Maximize the browser window for better visibility
        self.driver.maximize_window()
        # Set implicit wait for elements to load
        self.driver.implicitly_wait(10)

        # Initialize page objects for various site components
        self.main_page = BearStoreMainPage(self.driver)
        self.toolbar = BearStoreToolBar(self.driver)
        self.category_page = BearStoreCategoryPage(self.driver)
        self.product_page = BearStoreProductPage(self.driver)

    def test_page_transitions(self):
        """
        Test navigation and transitions between category, product, and homepage.
        """
        # Choose a random category and click it
        category_name = choice(self.main_page.categories()).text
        self.main_page.click_category(category_name)

        # Assert that the selected category name matches the current page
        self.assertEqual(category_name, self.category_page.get_category_name().text)

        # Scroll down a bit on the category page
        self.driver.execute_script("window.scrollBy(0, 100);")

        # Choose a random product and click it
        product = choice(self.category_page.product()).text
        self.category_page.click_product(product)

        # Assert that the selected product name matches the current product page
        self.assertEqual(self.product_page.get_product_name().text, product)

        # Navigate back to the category page via breadcrumbs
        self.product_page.inactive_breadcrumbs()[-1].click()

        # Return to the homepage by clicking the toolbar logo
        self.toolbar.toolbar_logo_click()

    def test_add_to_cart(self):
        """
        Adds multiple products to the shopping cart and verifies quantities.
        """
        # Call the helper function  to add  products
        quantity = randint(2, 5)
        self.add_random_product_to_cart(quantity)
        # Return to the homepage by clicking the toolbar logo
        self.toolbar.toolbar_logo_click()
        # Call the helper function  to add  products
        quantity = randint(2, 5)
        self.add_random_product_to_cart(quantity)

        # Check that the total quantity in the cart is correct
        """להמשיך מפה לבדיקה של כמות מוצרים"""

    def add_random_product_to_cart(self,random_quantity):
        """
        Adds a random product from a random category to the shopping cart
        with a random quantity, then returns to the homepage.
        """
        # Choose a random category and click it
        category_name = choice(self.main_page.categories()).text
        self.main_page.click_category(category_name)

        # Scroll down slightly on the category page
        self.driver.execute_script("window.scrollBy(0, 350);")

        # Choose a random product and click it
        products = self.category_page.product()
        product = choice(products).text
        self.category_page.click_product(product)
        self.driver.execute_script("window.scrollBy(0, 350);")
        # Change the quantity
        self.product_page.change_quantity(random_quantity)
        sleep(2)

        # Add the selected product to the shopping cart
        self.product_page.add_to_cart()

    def tearDown(self):
        """Clean up after the test."""
        # Wait for 2 seconds to observe results (if needed)
        sleep(2)
        # Close the browser to free up resources
        self.driver.quit()
